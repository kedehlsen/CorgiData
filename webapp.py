from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json
app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template('home.html')
        
        
@app.route("/p1") #annotations tell which function goes with which request
def render_page1():
    with open('election.json') as election:
        counties = json.load(election)
    return render_template('page1.html', options=get_county_options(counties))

@app.route("/getfact1")
def getfact1():
    with open('election.json') as election:
        counties = json.load(election)
    county = request.args["county"]
    return render_template("page1.html",  options=get_county_options(counties), dem_info = get_popular_dem(county, counties), rep_info = get_popular_rep(county, counties))
        
@app.route("/p2")
def render_page2():
    return render_template('page2.html')

@app.route("/p3")
def render_page3():
    return render_template('page3.html')

def get_county_options(counties):
    listOfCounties = []
    options = ""
    for data in counties:
        if data['Location']['County'] not in listOfCounties:
            listOfCounties.append(data['Location']['County'])
    for county in listOfCounties:
        options = options + Markup("<option value=\"" + county + "\">" + county + "</option>")
    return options

def get_popular_dem(county,counties):
    democrat={}
    returnDemName = "Bernie Sanders"
    returnDemNum = democrat['Bernie Sanders']
    returnDem =v""
    
    for person in counties[county]['Vote Data']:
        if counties[county]['Vote Data'][person]['Party'] == "Democrat":
            democrat[person] = counties[county]['Vote Data'][person]['Number of Votes']
    for people in democrat:
        if democrat[people] > returnDemNum:
            returnDemNum = democrat[people]
            returnDemName = people
            
    returnDem = returnDemName + " has the most votes in " + county + " with " + returnDemNum + " votes."
    return returnDem

def get_popular_rep(county,counties):
    republican={}
    returnRepName = "Ben Carson"
    returnRepNum = republican["Ben Carson"]
    returnRep = ""
    
    for person in counties[county]['Vote Data']:
        if counties[county]['Vote Data'][person]['Party'] == "Republican":
            republican[ person] = counties[county]['Vote Data'][person]['Number of Votes']
    for people in republican:
        if republican[people] > returnRepNum:
           returnRepNum = democrat[people]
           returnRepName = people
    returnRep = returnRepName + " has the most votes in " + county + " with " + returnRepNum + " votes."
    return returnRep



if __name__=="__main__":
        app.run(debug=True, port=54321)
