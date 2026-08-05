from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from PoGoDnIk import get_cache, main, to_cache
from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import to_display
from src.structures import CityData

APP = FastAPI()
CUR_PATH = Path(__file__).parent
TEMPLATES = Jinja2Templates(directory=CUR_PATH / "templates")
APP.mount("/static", StaticFiles(directory=CUR_PATH / "static"), name="static")
CONFIG = Path("configs.json")


# parsing config file
def get_config():
    config_parser = create_parser(CONFIG)
    return config_parser


# first page with a form to receive city name
@APP.get("/")
async def web_conclusion(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="index.html")


@APP.post("/")
async def city_redirect(city_name: str = Form(min_length=2)):
    return RedirectResponse(
        url=city_name,
        status_code=303,
    )


# second page with output of city data from cache or list with selection of city from found by geo provider
@APP.get("/{city_name}")
async def response(request: Request, city_name: str):
    config = get_config()
    geo_config = config.get_geo_config()
    timeout = config.get_timeout()
    weather_provider = config.get_weather_config().provider
    key = config.get_weather_config().api_key
    city_name_list = [city_name]
    cache = get_cache(city_name_list, timeout)
    if cache and (isinstance(cache[0], CityData)):
        text = to_display(cache[0])
        cityid = cache[0].weather_data.cityid
        match weather_provider:
            case "openweather":
                return TEMPLATES.TemplateResponse(
                    request=request,
                    name="data_ow.html",
                    context={"data": text, "key": key, "cityid": cityid},
                )
            case "openmeteo":
                return TEMPLATES.TemplateResponse(
                    request=request, name="data_om.html", context={"data": text}
                )
    else:
        geo_provider = create_geo_provider(geo_config, city_name_list[0])
        await geo_provider.request()
        city_list = geo_provider.response
        town_list = dict()
        for elem in city_list:
            town_list[city_list.index(elem) + 1] = (
                f"name: {elem['name']}, country: {elem['country']}, state: {elem.get('state', '')}"
            )
        return TEMPLATES.TemplateResponse(
            request=request,
            name="response.html",
            context={"city_list": town_list, "city_name": city_name_list[0]},
        )


# third page with output of data of selected city and writing these data to DB and output file
@APP.get("/{city_name}/{num}")
async def data(request: Request, num: int, city_name: str):
    city_name_list = [city_name]
    output = Path(CUR_PATH / "out.csv")
    config = get_config()
    weather_config = config.get_weather_config()
    weather_provider = config.get_weather_config().provider
    key = config.get_weather_config().api_key
    geo_config = config.get_geo_config()
    city_data, cache_data = await main(
        geo_config, weather_config, city_name_list, num - 1
    )
    await to_cache(cache_data, output)
    data_template = to_display(city_data[0])
    cityid = city_data[0].weather_data.cityid
    match weather_provider:
        case "openweather":
            return TEMPLATES.TemplateResponse(
                request=request,
                name="data_ow.html",
                context={"data": data_template, "key": key, "cityid": cityid},
            )
        case "openmeteo":
            return TEMPLATES.TemplateResponse(
                request=request,
                name="data_om.html",
                context={"data": data_template},
            )


# providers exceptions page
@APP.exception_handler(ProviderNoDataError)
@APP.exception_handler(ProviderCreationError)
async def provider_exception_handler(request: Request, exc: Exception):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="exceptions.html",
        context={"message": str(exc)},
        status_code=HTTP_400_BAD_REQUEST,
    )


#  config file exception page
@APP.exception_handler(FileNotFoundError)
async def config_exception_handler(request: Request, exc: FileNotFoundError):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="exceptions.html",
        context={"message": f"Config file not found: {exc.filename}"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
