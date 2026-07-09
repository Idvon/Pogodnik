from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from PoGoDnIk import get_cache, main, to_cache
from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import to_display
from src.structures import CityData

APP = FastAPI()
TEMPLATES = Jinja2Templates(directory="templates")
APP.mount("/static", StaticFiles(directory="static"), name="static")
CONFIG = Path("config.json")


# parsing config file
def get_config():
    if not CONFIG.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(CONFIG)
    return config_parser


# first page with a form to receive city name
@APP.get("/")
async def web_conclusion(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="index.html")


@APP.post("/")
async def city_redirect(request: Request):
    city_name = await request.form()
    return RedirectResponse(
        url=str(request.url_for("response", city_name=city_name["city_name"])),
        status_code=303,
    )


# second page with output of city data from cache or list with selection of city from found by geo provider
@APP.get("/response/{city_name}")
async def response(request: Request, city_name: str):
    try:
        geo_config = get_config().get_geo_config()
        timeout = get_config().get_timeout()
        weather_provider = get_config().get_weather_config().provider
        key = get_config().get_weather_config().api_key
        city_name_list = [city_name]
        cache = get_cache(city_name_list, timeout)
        if cache and (type(cache[0]) is CityData):
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
    except (ProviderNoDataError, ProviderCreationError) as error:
        return TEMPLATES.TemplateResponse(
            request=request, name="exceptions.html", context={"message": error}
        )


# third page with output of data of selected city and writing these data to DB and output file
@APP.get("/data/{num}/{city_name}")
async def data(request: Request, num: int, city_name: str):
    try:
        city_name_list = [city_name]
        output = Path("out.csv")
        weather_config = get_config().get_weather_config()
        weather_provider = get_config().get_weather_config().provider
        key = get_config().get_weather_config().api_key
        geo_config = get_config().get_geo_config()
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
    except (ProviderNoDataError, ProviderCreationError) as error:
        return TEMPLATES.TemplateResponse(
            request=request, name="exceptions.html", context={"message": error}
        )
