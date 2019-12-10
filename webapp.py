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
    return render_template('page1.html', stateoptions=get_state_options(counties),options=get_county_options(counties))

@app.route("/get_state")
def get_state():
    with open('election.json') as election:
        counties = json.load(election)
    state = request.args["state"]

    return render_template("page1.html",  stateoptions=get_state_options(counties), options=get_county_options(counties))

@app.route("/getfact1")
def getfact1():
    with open('election.json') as election:
        counties = json.load(election)
    state = request.args["state"]
    county = request.args["county"]

    return render_template("page1.html", stateoptions=get_state_options(counties), options=get_county_options(state, counties), dem_info = get_popular_dem(county, counties), rep_info = get_popular_rep(county, counties))
        
@app.route("/p2")
def render_page2():
    return render_template('page2.html')

@app.route("/p3")
def render_page3():
    return render_template('page3.html')

def get_county_options(state, counties):
    listOfCounties = []
    options = ""
    for data in counties:
        if data['Location']['County'] not in listOfCounties:
            if data['Location']['State'] == state:
                listOfCounties.append(data['Location']['County'])
    for county in listOfCounties:
        options = options + Markup("<option value=\"" + county + "\">" + county + "</option>")
    return options

def get_state_options(counties):
    listOfStates = []
    options = ""
    for data in counties:
        if data['Location']['State'] not in listOfStates:
            listOfStates.append(data['Location']['State']) 
   #maybe try to alphabetize
    for state in listOfStates:
        options = options + Markup("<option value=\"" + state + "\">" + state + "</option>")
    return options

def get_popular_dem(county,counties):
    democrat={}
    
    countyData = {}
    
    for c in counties:
        if c["Location"]["County"] == county:
            countyData = c
    
    for person in countyData["Vote Data"]:
        if countyData["Vote Data"][person]['Party'] == "Democrat":
            democrat[person] = countyData["Vote Data"][person]['Number of Votes']
    returnDemName = "Bernie Sanders"
    returnDemNum = democrat['Bernie Sanders']
    returnDem =""
    for people in democrat:
        if democrat[people] > returnDemNum:
            returnDemNum = democrat[people]
            returnDemName = people
            
    returnDem = returnDemName + " has the most votes in " + county + " with " + str(returnDemNum) + " votes."
    return returnDem

def get_popular_rep(county,counties):
    republican={}
    
    countyData = {}
    
    for c in counties:
        if c["Location"]["County"] == county:
            countyData = c
    
    for person in countyData["Vote Data"]:
        if countyData["Vote Data"][person]['Party'] == "Republican":
            republican[person] = countyData["Vote Data"][person]['Number of Votes']
    returnRepName = "Ben Carson"
    returnRepNum = republican["Ben Carson"]
    returnRep = ""
    for people in republican:
        if republican[people] > returnRepNum:
           returnRepNum = republican[people]
           returnRepName = people
    returnRep = returnRepName + " has the most votes in " + county + " with " + str(returnRepNum) + " votes."
    return returnRep

def get_counties_in_state(state,counties):
    counties_of_state = {}
    
    for s in counties:
        if s['Location']['State'] == state:
            counties_of_state = s
            
    return counties_of_state


if __name__=="__main__":
        app.run(debug=True, port=54321)
