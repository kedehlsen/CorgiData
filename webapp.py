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

def get_interesting_fact(county,counties):
    republican={}
    democrat={}
    returnVal= ""
    for data in counties:
        for person in data['Vote Data']:
            if data['Vote Data'][person]['Party'] == "Republican":
                republican[person] = data['Vote Data'][person]['Number of Votes']
            elif data['Vote Data'][person]['Party'] == "Democrat":
                democrat[person] = data['Vote Data'][person]['Number of Votes']
    if 
    return returnVal



if __name__=="__main__":
        app.run(debug=True, port=54321)
