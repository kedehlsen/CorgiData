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
    if "state" in request.args:
        state = request.args["state"]
        render = render_template('page1.html', stateoptions=get_state_options(counties,""),options=get_county_options("","",counties))
    else:
        render = render_template('page1.html', stateoptions=get_state_options(counties,""))
    return render



@app.route("/getfact1")
def getfact1():
    with open('election.json') as election:
        counties = json.load(election)
    
  
    if "state" in request.args:
        state = request.args["state"]
        if "county" in request.args:
            county = request.args["county"]
            render= render_template("page1.html", stateoptions=get_state_options(counties,state), options=get_county_options(county, state, counties), dem_info = get_popular_dem(state, county, counties), rep_info = get_popular_rep(state, county, counties), state_input=state)
        else:
            render = render_template('page1.html', stateoptions=get_state_options(counties,state),options=get_county_options("", state,counties), state_input=state)
    else:
        render = render_template('page1.html', stateoptions=get_state_options(counties,""))
    return render
        
@app.route("/p2") #THIS IS WHERE YOU ACTUALLY ARE, Make a graph of the amount of total repub votes vs total dem votes YOU can delete the bottom stuff, idk if it works
def render_page2():
    with open('election.json') as election:
        counties = json.load(election)
    if "state" in request.args:
        state = request.args["state"]
        render = render_template('page1.html', stateoptions=get_state_options(counties,""),options=get_county_options("","",counties))
    else:
        render = render_template('page1.html', stateoptions=get_state_options(counties,""))
    return render

@app.route("/p3")
def render_page3():
    return render_template('page3.html')

def get_county_options(county_selected, state_selected, counties):
    listOfCounties = []
    options = ""
    for data in counties:
        if data['Location']['County'] not in listOfCounties:
            if data['Location']['State'] == state_selected:
                listOfCounties.append(data['Location']['County'])
    for county in listOfCounties:
        print(county)
        if (county_selected == "") or not(county == county_selected):
            options = options + Markup("<option value=\"" + county + "\">" + county + "</option>")
        else:
           options = options + Markup("<option value=\"" + county + "\"" + " selected" + ">" + county + "</option>")
    return options

def get_state_options(counties,state_selected):
    listOfStates = []
    options = ""
    for data in counties:
        if data['Location']['State'] not in listOfStates:
            listOfStates.append(data['Location']['State']) 
   #maybe try to alphabetize
    for state in listOfStates:
        if (state_selected == "") or not(state == state_selected):
            options = options + Markup("<option value=\"" + state + "\">" + state + "</option>")
        else:
           options = options + Markup("<option value=\"" + state + "\"" + " selected" + ">" + state + "</option>")
    return options

def get_popular_dem(state,county,counties):
    democrat={}
    
    countyData = {}
    for c in counties:
        if c["Location"]["State"] == state:
            if c["Location"]["County"] == county:
                countyData = c
    #here is what YOU WERE WORKING ON
    
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

def get_popular_rep(state,county,counties):
    republican={}
    
    countyData = {}
    
    for c in counties:
        if c["Location"]["State"] == state:
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



if __name__=="__main__":
        app.run(debug=True, port=54321)
