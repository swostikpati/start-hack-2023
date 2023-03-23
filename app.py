import streamlit as st
import streamlit.components.v1 as components
import requests
import urllib
import json
from IPython.core.display import display, HTML, JSON
from types import SimpleNamespace
import logging
import plotly.graph_objects as go
import webbrowser
import datetime

############ page config
st.set_page_config(
    page_title="FinVerse - Team Cutting Edge - START Hack 2023",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nathanyaqueby/start-hack-2023',
        'Report a bug': "https://github.com/nathanyaqueby/start-hack-2023",
        'About': """
        In today's world, financial literacy is more important than ever. Unfortunately, many people lack access to the resources and knowledge needed to manage their finances effectively. This is where FinVerse comes in.
        FinVerse is designed to make financial literacy accessible to everyone. By using virtual reality technology, we have created a platform that is engaging, interactive, and easy to use. Our application is specifically designed to help increase inclusivity of financial literacy by making it accessible to the common people.
        With FinVerse, users can explore different financial concepts and strategies in a way that is both fun and informative. Our application allows users to simulate real-life financial scenarios, experiment with different investment strategies, and learn about the basics of budgeting and saving.
        Our team has worked tirelessly to ensure that FinVerse is user-friendly, visually appealing, and most importantly, effective. By combining the power of virtual reality with expert financial advice, we believe that FinVerse has the potential to revolutionize financial literacy education.
        We are excited to participate in this hackathon and look forward to showcasing the power of FinVerse.
        """
    }
)

st.markdown("## Virtual Reality-Based Financial Literacy Web Application")
st.markdown("Welcome to *_FinVerse_*! "
            "Dive into the VR world by running the generator on the left sidebar and use keypads to walk through your financial universe."
            " Read more about our project on [GitHub](https://github.com/nathanyaqueby/start-hack-2023). Enjoy!")

##############################################

logger = logging.getLogger()
logger.setLevel(logging.INFO) # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

display(HTML("<style>.container { width:90% !important; }</style>"))

class FinancialDataAPI:
    def __init__(self):
        self.url = 'https://web.api.six-group.com/api/findata'
        
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "api-version": "2022-06-01"
        }
        self.session = requests.session()
        certificate_path = 'ch52991-hackathon1'
        self.session.cert = (f'{certificate_path}/signed-certificate.pem', f'{certificate_path}/private-key.pem')
    
    def http_request(self, end_point:str, query_string:dict) -> str:
        # Make an HTTP request and send the raw response
        try:
            http_request = f"{self.url}{end_point}?{urllib.parse.urlencode(query_string)}"
            
            r = self.session.get(http_request, headers=self.headers) #, verify='./six-certificate/certificate.pem')
            if str(r.status_code)[0] != "2":
                logging.debug(f"HTTP{r.status_code}: {r.content}")
            else:
                logging.debug(f"HTTP{r.status_code}: {json.dumps(json.loads(r.content), indent=2)}")
                
            return r
        except requests.exceptions.SSLError as err:
            logging.error(f"Error - {http_request}:\r\n{err}")
            raise(Exception(str(err)))

    def http_request_with_scheme_id(self, end_point:str, scheme:str, ids:list) -> str:
        query_string = query_string = { 
            'scheme': scheme,
            'ids': ",".join(ids)
        }
        return self.http_request(end_point, query_string)        
            
    def _convert_response_to_object(self, http_response):
        if str(http_response.status_code)[0] == "2":
            obj = json.loads(http_response.content, object_hook=lambda d: SimpleNamespace(**d))
            return obj
        return None
            
    def text_search(self, query:str) -> object:
        end_point = "/v1/searchInstruments"
        #end_point = "/search/v1/"
        query_string = { 'query': query }
        resp = self.http_request(end_point, query_string)
        
        return self._convert_response_to_object(resp)
    
    def instrument_summary(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/referenceData/instrumentSummary"
        #end_point = "/v1/summary/instruments"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_symbology(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/referenceData/instrumentSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_BASELIII_HQLA_EU(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/_regulatoryData/baseliiihqlaEU"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_BASELIII_HQLA_CH(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/_regulatoryData/baseliiihqlaCH"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_SFDR(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/SFDRInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_TAXONOMY(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/EUTaxonomyInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_EUESGMANUFACTURER(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/EUESGManufacturer"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)
    
    def institution_summary(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/referenceData/institutionSummary"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def institution_symbology(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/referenceData/institutionSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)
    
    def institution_SFDR(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/esg/SFDRInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def institution_TAXONOMY(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/esg/EUTaxonomyInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def market_summary(self, scheme:str, markets: list):
        end_point = "/v1/markets/referenceData/marketSummary"
        resp = self.http_request_with_scheme_id(end_point, scheme, markets)
        return self._convert_response_to_object(resp)
    
    def market_symboloy(self, scheme:str, markets: list):
        end_point = "/v1/markets/referenceData/marketSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, markets)
        return self._convert_response_to_object(resp)

    def listing_EoDTimeseries(self, scheme:str, listings: list, from_date:str, to_date:str = ''):
        end_point = "/v1/listings/marketData/eodTimeseries"
        query_string = query_string = { 
            'scheme': scheme,
            'ids': ",".join(listings),
            'from': from_date,
            'to': to_date
        }
        resp = self.http_request(end_point, query_string)    
        return self._convert_response_to_object(resp)
    
findata = FinancialDataAPI()

######################### print_object_attributes #########################

def print_object_attributes_text(valors, bcs, obj:object, tab_level:int=0, min_attr_length:int=30):
    if obj is None: return
    space_sep = "  "
    space = space_sep*tab_level
    
    if type(obj) == list:
        for o in obj:
            if type(o) == object or type(o) == SimpleNamespace:
                print_object_attributes_text(valors, bcs, o, tab_level+1, min_attr_length)
    else:
        for attr, value in obj.__dict__.items():
            if type(value) == object or type(value) == SimpleNamespace or type(value) == list:
                # st.markdown(f"{space}{attr}")

                adjusted_min_attr_length = min_attr_length - (len(space_sep)*(tab_level+1))
                if adjusted_min_attr_length < 0: adjusted_min_attr_length = 0
                print_object_attributes_text(valors, bcs, value, tab_level+1, adjusted_min_attr_length)
            else:
                if attr == "valor":
                    valors.append(value)
                if attr == "bc":
                    bcs.append(value)
                # st.markdown(f"{space}{attr:<{min_attr_length}}: {value}")    

    # if length of valors and bcs is greater than 0, return them
    if len(valors) > 0 and len(bcs) > 0:
        return valors, bcs 

######################### print_object_attributes (time series) ######################### 

def print_object_attributes_timeseries(highs, lows, obj:object, tab_level:int=0, min_attr_length:int=30):
    if obj is None: return
    space_sep = "  "
    space = space_sep*tab_level
    
    if type(obj) == list:
        for o in obj:
            if type(o) == object or type(o) == SimpleNamespace:
                print_object_attributes_timeseries(highs, lows, o, tab_level+1, min_attr_length)
                # print()
            # else:
            #     print(f"{space}{o:<{min_attr_length}}")
    else:
        for attr, value in obj.__dict__.items():
            if type(value) == object or type(value) == SimpleNamespace or type(value) == list:
                # print(f"{space}{attr}")

                adjusted_min_attr_length = min_attr_length - (len(space_sep)*(tab_level+1))
                if adjusted_min_attr_length < 0: adjusted_min_attr_length = 0
                print_object_attributes_timeseries(highs, lows, value, tab_level+1, adjusted_min_attr_length)
            else:
                if attr == "high":
                    highs.append(value)
                if attr == "low":
                    lows.append(value) 
    
    # if length of dates and volumes is greater than 0, return them
    return highs, lows

######################### DASHBOARD #########################    

# add image to the sidebar
st.sidebar.image("SIX_CUTTINGEDGE.png", use_column_width=True)

with st.sidebar.form(key='Form1'):
    # create a sidebar with a submit button
    st.title("📈 3D Stock Dashboard")

    options = st.multiselect(
    'Which companies would you like to see?',
    ['DKSH', 'Tesla', 'Amazon', 'Nike', 'Apple', 'Google', 'Samsung', 'Meta', 'Boeing', 'SIX'],
    default=['Apple', 'Google', 'Samsung', 'Meta', 'Boeing', 'SIX']
    )

    # add an input field for the user to enter the starting date
    start_date = st.date_input("Enter a start date", datetime.date(2022, 7, 1), max_value=datetime.date(2023, 3, 21))

    # save the date in the format YYYY-MM-DD
    start_date = start_date.strftime("%Y-%m-%d")

    # add an input field for the user to enter the starting date
    end_date = st.date_input("Enter an end date", datetime.date(2023, 3, 22), max_value=datetime.date(2023, 3, 22))

    # save the date in the format YYYY-MM-DD
    end_date = end_date.strftime("%Y-%m-%d")

    # add a submit button to the sidebar
    submit_button = st.form_submit_button(label='Generate VR world', use_container_width=True, type="primary")

    # add tips to the sidebar
    st.markdown("""<b>💡 Tips:</b><br>
                Use VR glasses to experience the world in 3D!
                Try our [randomly generated world](https://www.sararutz.ch/cuttingedge/index.html).
                """, unsafe_allow_html=True)

st.sidebar.image("START_Logo.png", use_column_width=True)

if submit_button:

    with st.spinner('Loading...'):

        video_file = open('trailer.mp4', 'rb')
        video_bytes = video_file.read()

        diffs = []

        # for each company in the list, get the company information
        for company in options:

            valors = []
            bcs = []
            highs = []
            lows = []

            count = 0

            # while highs and lows are empty, get the company information
            while len(highs) == 0 and len(lows) == 0:

                try:
                    obj = findata.text_search(company)
                    valors, bcs = print_object_attributes_text(valors, bcs, obj)

                    # get the EoD timeseries for the company
                    obj = findata.listing_EoDTimeseries("VALOR_BC", [f"{valors[count]}_{bcs[count]}"], start_date, end_date)
                    highs, lows = print_object_attributes_timeseries(highs, lows, obj)
                
                except:
                    st.write("Error", company, count)

                count += 1

            # append the difference between each high and low to the list "decimals"
            decimals = [(highs[i]-lows[i]) for i in range(len(highs))]
            
            # divide all elements in decimals by the maximum element in decimals
            decimals = [i/max(decimals) for i in decimals]

            # append the difference between each high and low to the list "diffs"
            diffs.append(decimals)

        # st.write("Differences: ", diffs)

        components.html('<iframe src="https://www.sararutz.ch/cuttingedge/index.html" style="position: absolute; height: 100%; width: 100%; border: none"></iframe>', height=700)

        # components.html(
        #     '''
        #     <html lang="en">
        #         <head>
        #             <title>WebXR Application</title>
        #             <link rel="icon" type="image/png" href="favicon.ico"/>
        #             <meta name="description" content="3D Application">
        #             <meta charset="utf-8">
        #             <meta http-equiv="X-UA-Compatible" content="IE=edge">
        #             <meta name="viewport" content="width=device-width, initial-scale=1">
        #             <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
        #             <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.0/dist/aframe-extras.min.js"></script>
        #             <script type="text/javascript" src="js/webxr.js"></script>
        #             <script type="text/javascript" src="js/joystick.js"></script>
        #             <script type="text/javascript" src="js/camera-cube-env.js"></script>
                    
        #             <link rel="stylesheet" type="text/css" href="style.css">
        #         </head>
        #         <body onload="init();">
        #             <a-scene   shadow="type: basic; autoUpdate: false;" renderer="antialias: false; colorManagement: false; physicallyCorrectLights: false;">
        #                 <!-- Assets -->
        #                 <a-assets>
        #                     <a-asset-item id="amazon" src="./assets/amazon.gltf"></a-asset-item>
        #                     <a-asset-item id="apple" src="./assets/apple.gltf"></a-asset-item>
        #                     <a-asset-item id="boeing" src="./assets/boeing.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube" src="./assets/Cube.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.001" src="./assets/Cube.001.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.002" src="./assets/Cube.002.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.003" src="./assets/Cube.003.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.004" src="./assets/Cube.004.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.005" src="./assets/Cube.005.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.006" src="./assets/Cube.006.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.007" src="./assets/Cube.007.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.008" src="./assets/Cube.008.gltf"></a-asset-item>
        #                     <a-asset-item id="Cube.009" src="./assets/Cube.009.gltf"></a-asset-item>
        #                     <a-asset-item id="deloitte " src="./assets/deloitte .gltf"></a-asset-item>
        #                     <a-asset-item id="DKSH" src="./assets/DKSH.gltf"></a-asset-item>
        #                     <a-asset-item id="google " src="./assets/google .gltf"></a-asset-item>
        #                     <a-asset-item id="meta" src="./assets/meta.gltf"></a-asset-item>
        #                     <a-asset-item id="nike " src="./assets/nike .gltf"></a-asset-item>
        #                     <a-asset-item id="Plane" src="./assets/Plane.gltf"></a-asset-item>
        #                     <a-asset-item id="samsung " src="./assets/samsung .gltf"></a-asset-item>
        #                     <a-asset-item id="six" src="./assets/six.gltf"></a-asset-item>
        #                     <img id="sky"                 src="./resources/sky.jpg">
        #                     <img id="icon-play"           src="./resources/play.png">
        #                     <img id="icon-pause"          src="./resources/pause.png">
        #                     <img id="icon-play-skip-back" src="./resources/play-skip-back.png">
        #                     <img id="icon-mute"           src="./resources/mute.png">
        #                     <img id="icon-volume-low"     src="./resources/volume-low.png">
        #                     <img id="icon-volume-high"    src="./resources/volume-high.png">
        #                 </a-assets>

        #                 <!-- Entities -->
                        
        #                 <a-entity id="#amazon" gltf-model="#amazon"  scale="1 1 1" position="1.1128391027450562 4.325775146484375 14.492897033691406" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#apple" gltf-model="#apple"  scale="1 1 1" position="0.8324559926986694 4.1404709815979 2.7704522609710693" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#boeing" gltf-model="#boeing"  scale="1 1 1" position="0.8865522146224976 5.622444152832031 11.70455551147461" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube" gltf-model="#Cube"  scale="1 1 1" position="-0.22648416459560394 2.8150224685668945 2.756023645401001" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.001" gltf-model="#Cube.001"  scale="1 1 1" position="-0.22648416459560394 3.5149612426757812 5.844135284423828" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.002" gltf-model="#Cube.002"  scale="1 1 1" position="0.0 3.4247751235961914 -0.055373240262269974" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.003" gltf-model="#Cube.003"  scale="1 1 1" position="-0.22648416459560394 3.226078987121582 -2.9352900981903076" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.004" gltf-model="#Cube.004"  scale="1 1 1" position="-0.22648416459560394 3.5149612426757812 -6.4891157150268555" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.005" gltf-model="#Cube.005"  scale="1 1 1" position="-0.22648416459560394 2.8150224685668945 8.732294082641602" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.006" gltf-model="#Cube.006"  scale="1 1 1" position="-0.22648416459560394 2.8150224685668945 14.422906875610352" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.007" gltf-model="#Cube.007"  scale="1 1 1" position="-0.22648416459560394 3.5149612426757812 11.534748077392578" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.008" gltf-model="#Cube.008"  scale="1 1 1" position="-0.22648416459560394 3.226078987121582 -12.412830352783203" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Cube.009" gltf-model="#Cube.009"  scale="1 1 1" position="0.0 3.4247751235961914 -9.532913208007812" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#deloitte " gltf-model="#deloitte "  scale="1 1 1" position="0.7883981466293335 4.892899513244629 -2.914421558380127" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#DKSH" gltf-model="#DKSH"  scale="1 1 1" position="0.846261739730835 4.84961462020874 -12.34501838684082" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#google " gltf-model="#google "  scale="1 1 1" position="1.0024456977844238 5.113276481628418 -0.0" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#meta" gltf-model="#meta"  scale="1 1 1" position="1.2688511610031128 5.42894983291626 -9.600595474243164" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#nike " gltf-model="#nike "  scale="1 1 1" position="0.7864484786987305 5.125548362731934 5.912516117095947" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#Plane" gltf-model="#Plane"  scale="1 1 1" position="0.0 0.0 -0.0" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#samsung " gltf-model="#samsung "  scale="1 1 1" position="0.7934677004814148 4.5191802978515625 8.834068298339844" visible="true" shadow="cast: false" ></a-entity>
        #                 <a-entity id="#six" gltf-model="#six"  scale="1 1 1" position="0.8898735046386719 5.763146877288818 -6.4537248611450195" visible="true" shadow="cast: false" ></a-entity>

        #                 <!-- Camera -->
        #                 <a-entity id="player" 
        #                     position="0 -0.2 0" 
        #                     movement-controls="speed: 0.10000000149011612;">
        #                     <a-entity id="camera" 
        #                         camera="near: 0.001" 
        #                         position="0 1.7000000476837158 0" 
        #                         look-controls="pointerLockEnabled: true">
        #                             <a-entity id="cursor" cursor="fuse: false;" animation__click="property: scale; startEvents: click; easing: easeInCubic; dur: 50; from: 	0.1 0.1 0.1; to: 1 1 1"
        #                                 position="0 0 -0.1"
        #                                 geometry="primitive: circle; radius: 0.001;"
        #                                 material="color: #CCC; shader: flat;"
        #                                 >
        #                             </a-entity>
        #                     </a-entity>
        #                         <a-entity id="leftHand" oculus-touch-controls="hand: left" vive-controls="hand: left"></a-entity>
        #                         <a-entity id="rightHand" laser-controls oculus-touch-controls="hand: right" vive-controls="hand: right" ></a-entity>
        #                 </a-entity>

        #                 <!-- Lights -->
                        
        #                 <a-entity position="0.5248908996582031 1.1606484651565552 -0.0" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="0.0 2.9586710929870605 2.8257946968078613" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.523449182510376 2.8169617652893066 6.309124946594238" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.5871739387512207 3.5962722301483154 -2.9193484783172607" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 2.711784601211548 8.935091972351074" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 3.973264455795288 -6.496705055236816" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 2.682612657546997 11.793471336364746" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 2.6372766494750977 14.843578338623047" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 3.0482330322265625 -9.426068305969238" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>
        #                 <a-entity position="-0.25771796703338623 1.8322162628173828 -12.441837310791016" light="castShadow:false; color:#ffffff; distance:40.0; type:point; intensity:1.0; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2;"></a-entity>

        #                 <!-- Sky -->
        #                 <a-sky color="#ECECEC"></a-sky>
        #             </a-scene>
        #         </body>
        #     </html>
        #     '''
        #     )

        with st.expander("For the stock market experts"):
            # plot the differences in a single graph with multiple lines (one for each company)
            fig = go.Figure()
            for i in range(len(diffs)):
                fig.add_trace(go.Scatter(x=[i for i in range(len(diffs[i]))], y=diffs[i], name=options[i]))
            fig.update_layout(title="Differences between highs and lows", xaxis_title="Days", yaxis_title="Differences")
            st.plotly_chart(fig, use_container_width=True)