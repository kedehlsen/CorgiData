from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def render_main():
    with open('election.json') as demographics_data:
        counties = json.load(election)
    return render_template('home.html', options=get_state_options(counties))

@app.route("/p1") #annotations tell which function goes with which request
def render_page1():
    return render_template('page1.html')

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



if __name__=="__main__":
        app.run(debug=True, port=54321)
