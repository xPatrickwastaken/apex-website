from flask import Flask, render_template, request, redirect, url_for, session, current_app

app = Flask(__name__)
# ⚠️ Change this in production to a strong random string!
app.secret_key = 'F9pU?)i@jg-6qa|ea=8kz&o7UR7h[*YF'  
VALID_PASSWORD = "xyzlebron"  # 🔐 Change this to your actual team password
import json
from datetime import datetime

# 📦 In-memory storage for demonstration. Replace with SQLite/SQLAlchemy later!
team_tips = {}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def handle_login():
    password = request.form.get('password')
    if password == VALID_PASSWORD:
        session['authenticated'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', login_error="Invalid password. Try again.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 🔐 Dashboard & Subsection Routes
@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))
    # ✅ Explicitly pass url_for to prevent Jinja2 context errors
    return render_template('dashboard.html', current_page='dashboard', url_for=current_app.url_for)

@app.route('/lootpaths')
def lootpaths():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))

    LOOT_DATA = {
        "World's Edge": {
            "thumb": "static/images/maps/wedge/wedge.png",
            "pois": [
            {"id": 1, "name": "Big Maude", "image": "static/images/maps/wedge/big_maude.png", "path": "filler"},
            {"id": 2, "name": "Countdown", "image": "static/images/maps/wedge/Countdown.png", "path": "filler"},
            {"id": 3, "name": "Dome", "image": "static/images/maps/wedge/dome.png", "path": "filler"},
            {"id": 4, "name": "East Village", "image": "static/images/maps/wedge/east_village.png", "path": "filler"},
            {"id": 5, "name": "Epicenter", "image": "static/images/maps/wedge/Epicenter.png", "path": "filler"},
            {"id": 6, "name": "Fragment", "image": "static/images/maps/wedge/fragment.png", "path": "filler"},
            {"id": 7, "name": "Geyser", "image": "static/images/maps/wedge/Geyser.png", "path": "filler"},
            {"id": 8, "name": "Launch Site", "image": "static/images/maps/wedge/Launch_Site.png", "path": "filler"},
            {"id": 9, "name": "Lava Fissure", "image": "static/images/maps/wedge/Lava_Fissure.png", "path": "filler"},
            {"id": 10, "name": "Mirage", "image": "static/images/maps/wedge/mirage.png", "path": "filler"},
            {"id": 11, "name": "Monument", "image": "static/images/maps/wedge/monument.png", "path": "filler"},
            {"id": 12, "name": "New Harvester", "image": "static/images/maps/wedge/new_Harvester.png", "path": "filler"},
            {"id": 13, "name": "Overlook", "image": "static/images/maps/wedge/overlook.png", "path": "filler"},
            {"id": 14, "name": "Sky East", "image": "static/images/maps/wedge/Sky_East.png", "path": "filler"},
            {"id": 15, "name": "Sky West", "image": "static/images/maps/wedge/sky_west.png", "path": "filler"},
            {"id": 16, "name": "Sorting Factory", "image": "static/images/maps/wedge/sorting_factory.png", "path": "filler"},
            {"id": 17, "name": "Stacks", "image": "static/images/maps/wedge/Stacks.png", "path": "filler"},
            {"id": 18, "name": "Staging", "image": "static/images/maps/wedge/staging.png", "path": "filler"},
            {"id": 19, "name": "Thermal Station", "image": "static/images/maps/wedge/Thermal_Station.png", "path": "filler"},
            {"id": 20, "name": "War Camp", "image": "static/images/maps/wedge/war_camp.png", "path": "filler"},
        ]},
        "Olympus": {
            "thumb": "static/images/maps/olympus/olympus.png",
            "pois": [
                {"id": 1, "name": "Bonsai Plaza", "image": "static/images/maps/olympus/bonsai_plaza.png", "path": "filler"},
                {"id": 2, "name": "Carrier", "image": "static/images/maps/olympus/carrier.png", "path": "filler"},
                {"id": 3, "name": "Clinic", "image": "static/images/maps/olympus/clinic.png", "path": "filler"},
                {"id": 4, "name": "Dockyard", "image": "static/images/maps/olympus/dockyard.png", "path": "filler"},
            {"id": 5, "name": "Elysium", "image": "static/images/maps/olympus/elysium.png", "path": "filler"},
            {"id": 6, "name": "Estates", "image": "static/images/maps/olympus/estates.png", "path": "filler"},
            {"id": 7, "name": "Fight Night", "image": "static/images/maps/olympus/fight_night.png", "path": "filler"},
            {"id": 8, "name": "Gardens", "image": "static/images/maps/olympus/gardens.png", "path": "filler"},
            {"id": 9, "name": "Gravity Engine", "image": "static/images/maps/olympus/gravity_engine.png", "path": "filler"},
            {"id": 10, "name": "Grow Towers", "image": "static/images/maps/olympus/grow_towers.png", "path": "filler"},
            {"id": 11, "name": "Hammond Labs", "image": "static/images/maps/olympus/hammond_labs.png", "path": "filler"},
            {"id": 12, "name": "Hydroponics", "image": "static/images/maps/olympus/hydroponics.png", "path": "filler"},
            {"id": 13, "name": "Icarus", "image": "static/images/maps/olympus/icarus.png", "path": "filler"},
            {"id": 14, "name": "New Power Grid", "image": "static/images/maps/olympus/new_Power_Grid.png", "path": "filler"},
            {"id": 15, "name": "New Solar Array", "image": "static/images/maps/olympus/new_Solar_Array.png", "path": "filler"},
            {"id": 16, "name": "Oasis", "image": "static/images/maps/olympus/oasis.png", "path": "filler"},
            {"id": 17, "name": "Phase Driver", "image": "static/images/maps/olympus/phase_driver.png", "path": "filler"},
            {"id": 18, "name": "Rift", "image": "static/images/maps/olympus/rift.png", "path": "filler"},
            {"id": 19, "name": "Sommers", "image": "static/images/maps/olympus/sommers.png", "path": "filler"},
            {"id": 20, "name": "Stabilizer", "image": "static/images/maps/olympus/stabilizer.png", "path": "filler"},
            {"id": 21, "name": "Terminal", "image": "static/images/maps/olympus/terminal.png", "path": "filler"},
            {"id": 22, "name": "Turbine", "image": "static/images/maps/olympus/turbine.png", "path": "filler"},
        ]},
        "Storm Point": {
            "thumb": "static/images/maps/sp/sp.png",
            "pois": [
                {"id": 1, "name": "Barometer", "image": "static/images/maps/sp/barometer.png", "path": "filler"},
                {"id": 2, "name": "Bean", "image": "static/images/maps/sp/Bean.png", "path": "filler"},
                {"id": 3, "name": "Cascade Falls", "image": "static/images/maps/sp/Cascade_Falls.png", "path": "filler"},
                {"id": 4, "name": "Cenote Cave", "image": "static/images/maps/sp/Cenote_Cave.png", "path": "filler"},
                {"id": 5, "name": "Checkpoint", "image": "static/images/maps/sp/checkpoint.png", "path": "filler"},
                {"id": 6, "name": "Cliffside","id": 7,"name": "Command Center","image": "static/images/maps/sp/command_center.png",("path"): "filler"},
                {"id": 8, "name": "Devastated Coast","image": "static/images/maps/sp/devastated_coast.png","path": "filler"},
                {"id": 9, "name":"Downed Beast","image":"static/images/maps/sp/Downed_beast.png","path":"filler"},
            {"id": 10, "name": "Echo HQ", "image": "static/images/maps/sp/Echo_HQ.png", "path": "filler"},
            {"id": 11, "name": "Launch Pad", "image": "static/images/maps/sp/Launch_Pad.png", "path": "filler"},
            {"id": 12, "name": "Lightning Rod", "image": "static/images/maps/sp/lightning_rod.png", "path": "filler"},
            {"id": 13, "name": "Mountain Lift", "image": "static/images/maps/sp/Mountain_Lift.png", "path": "filler"},
            {"id": 14, "name": "New Ceto Station", "image": "static/images/maps/sp/new_Ceto_Station.png", "path": "filler"},
            {"id": 15, "name": "New Coastal Camp", "image": "static/images/maps/sp/new_Costal_Camp.png", "path": "filler"},
            {"id": 16, "name": "New Jurassic", "image": "static/images/maps/sp/new_Jurrasic.png", "path": "filler"},
            {"id": 17, "name": "New Mill", "image": "static/images/maps/sp/new_Mill.png", "path": "filler"},
            {"id": 18, "name": "New Stormcatcher", "image": "static/images/maps/sp/new_Stormcatcher.png", "path": "filler"},
            {"id": 19, "name": "North Pad", "image": "static/images/maps/sp/North_Pad.png", "path": "filler"},
            {"id": 20, "name": "Pylon", "image": "static/images/maps/sp/pylon.png", "path": "filler"},
            {"id": 21, "name": "Wall", "image": "static/images/maps/sp/wall.png", "path": "filler"},
            {"id": 22, "name": "Zeus Station", "image": "static/images/maps/sp/zeus_station.png", "path": "filler"},
        ]},
        "E-District": {
            "thumb": "static/images/maps/ed/ed.png",
            "pois":
        [
            {"id": 1, "name": "Blossom Drive", "image": "static/images/maps/ed/Blossom_Drive.png", "path": "filler"},
            {"id": 2, "name": "Boardwalk", "image": "static/images/maps/ed/boardwalk.png", "path": "filler"},
            {"id": 3, "name": "Canal", "image": "static/images/maps/ed/canal.png", "path": "filler"},
            {"id": 4, "name": "City Hall", "image": "static/images/maps/ed/City_Hall.png", "path": "filler"},
            {"id": 5, "name": "Electro Dam", "image": "static/images/maps/ed/electro_dam.png", "path": "filler"},
            {"id": 6, "name": "Energy Bank", "image": "static/images/maps/ed/energy-bank.png", "path": "filler"},
            {"id": 7, "name": "Galleria", "image": "static/images/maps/ed/galleria.png", "path": "filler"},
            {"id": 8, "name": "Heights", "image": "static/images/maps/ed/Heights.png", "path": "filler"},
            {"id": 9, "name": "Humbert", "image": "static/images/maps/ed/humbert.png", "path": "filler"},
            {"id": 10, "name": "Lotus", "image": "static/images/maps/ed/Lotus.png", "path": "filler"},
            {"id": 11, "name": "Neon Square", "image": "static/images/maps/ed/Neon_Square.png", "path": "filler"},
            {"id": 12, "name": "New Draft Point", "image": "static/images/maps/ed/new_Draft_Point.png", "path": "filler"},
            {"id": 13, "name": "New Viaduct", "image": "static/images/maps/ed/new_Viaduct.png", "path": "filler"},
            {"id": 14, "name": "Old Town", "image": "static/images/maps/ed/Old_Town.png", "path": "filler"},
            {"id": 15, "name": "Resort", "image": "static/images/maps/ed/Resort.png", "path": "filler"},
            {"id": 16, "name": "Settlement", "image": "static/images/maps/ed/settlement.png", "path": "filler"},
            {"id": 17, "name": "Shipyard", "image": "static/images/maps/ed/Shipyard.png", "path": "filler"},
            {"id": 18, "name": "Stadium", "image": "static/images/maps/ed/stadium.png", "path": "filler"},
            {"id": 19, "name": "Street Market", "image": "static/images/maps/ed/Street_Market.png", "path": "filler"},
            {"id": 20, "name": "Uptown", "image": "static/images/maps/ed/uptown.png", "path": "filler"},
        ]}
    }

    return render_template('lootpaths.html', loot_data=LOOT_DATA, current_page="lootpaths", section_title="Loot Paths", url_for=current_app.url_for)

@app.route('/team-comps')
def team_comps():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))
    return render_template('team_comps.html', section_title="Team Compositions", url_for=current_app.url_for)

@app.route('/map-data')
def map_data():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))
    return render_template('map_data.html', section_title="Spawn & Map Data", url_for=current_app.url_for)

@app.route('/gun-data')
def gun_data():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))
    return render_template('gun_data.html', section_title="Gun & Loadout Data", url_for=current_app.url_for)

@app.route('/socials')
def socials():
    if not session.get('authenticated'): 
        return redirect(url_for('home'))
    return render_template('socials.html', section_title="Team Socials", url_for=current_app.url_for)

@app.route('/api/save-tip', methods=['POST'])
def save_tip():
    # Handle JSON POST data from the browser
    data = request.get_json() or request.form
    
    map_name = data.get('map')
    poi_id = data.get('id')
    tip_text = data.get('tipText')

    if not all([map_name, poi_id, tip_text]):
        return json.dumps({"error": "Missing required fields"}), 400

    # Store the tip
    team_tips.setdefault(map_name, {}).setdefault(poi_id, []).append({
        "text": tip_text.strip(),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return json.dumps({"status": "success", "message": f"Tip saved for {map_name} - POI {poi_id}"})

if __name__ == '__main__':
    app.run(debug=True)
