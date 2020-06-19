import secrets
import os
from flask import render_template,redirect,url_for,flash,request,abort
from . import main
from .forms import UploadBlog,Comments,UpdateSettings
from ..models import User,Blogs,Comment
from ..request import get_quote
from PIL import Image


