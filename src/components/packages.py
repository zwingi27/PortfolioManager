# Python packages used in this Tool:
# from sklearn.preprocessing import MinMaxScaler, minmax_scale, StandardScaler, OneHotEncoder
# from sklearn.impute import SimpleImputer
# from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import time
from datetime import datetime,timedelta
import warnings
warnings.simplefilter("ignore")
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.tools as tools
from IPython.display import HTML
import plotly.express as px
from itertools import combinations
import json

import plotly.tools as tool
import plotly.subplots as subplots
import base64
import io
from dash.exceptions import PreventUpdate
import dash
from dash import Dash, html, dash_table
from dash.html.Q import Q
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Button import Button
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import io

from components.dataUploader import DataUploader
from classes.databaseClass import PostgressHandler