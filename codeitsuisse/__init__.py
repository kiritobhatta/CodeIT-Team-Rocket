from flask import Flask;
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.saladSpree
import codeitsuisse.routes.inventoryManagement
import codeitsuisse.routes.clean_floor
import codeitsuisse.routes.optimizedportfolio
import codeitsuisse.routes.socialDistancing

