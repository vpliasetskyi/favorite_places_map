

import folium
import webbrowser
import math


class Place:
    
    
    def __init__(self, name, latitude, longitude):
        # Attributes (data)
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
   
    
    def get_info(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
    
    
    def distance_to(self, other_place):
        # Difference in latitude and longitude
        lat_diff = self.latitude - other_place.latitude
        lon_diff = self.longitude - other_place.longitude
        
        # Simple Euclidean distance (good enough for learning)
        # 1 degree ≈ 111 km
        distance_km = math.sqrt(lat_diff**2 + lon_diff**2) * 111
        
        return round(distance_km, 2)
   
    
    def get_marker_color(self):
        return "blue"
   
    def get_popup_text(self):
        return f"<b>{self.name}</b><br>Click for more info!"



class Restaurant(Place):
    
    def __init__(self, name, latitude, longitude, food_type):
        #  Call the parent constructor
        super().__init__(name, latitude, longitude)
        #  Store food_type as an attribute
        self.food_type = food_type
    
    #  Override get_popup_text()
    # Should return: "<b>RESTAURANT: name</b><br>Food: food_type"
    def get_popup_text(self):
        return f"<b>RESTAURANT:{self.name}</b><br>Food: {self.food_type}"        


    # Override get_marker_color()
    # Should return: "red"
    def get_marker_color(self):
        return "red"


class Park(Place):
   
    def __init__(self, name, latitude, longitude, has_playground):
        #  Call the parent constructor
        #  Store has_playground as an attribute
        super().__init__(name, latitude, longitude)
        self.has_playground = has_playground
    
    #  Override get_popup_text()
    # Should include playground info: "Playground: Yes/No"
    def get_popup_text(self):
        playground_bool = "Yes" if self.has_playground else "No"
        return f"<b>Park:{self.name}</b><br> Playground:{playground_bool}"
    
    
#  Override get_marker_color()
# Should return: "green"
    def get_marker_color(self):
        return "green"


class Museum(Place):
    
    def __init__(self, name, latitude, longitude, entry_fee):
    #  Call the parent constructor
    #  Store entry_fee as an attribute
        super().__init__(name,latitude, longitude)
        self.entry_fee = entry_fee    
    
    #  Override get_popup_text()
    # Should include: "Entry: €X"
    def get_popup_text(self):
        return f"<b>{self.name}</b><br>Entry: €{self.entry_fee}"
    #  Override get_marker_color()
    # Should return: "purple"
    def get_marker_color(self):
        return "purple"



class Cafe(Restaurant):
 
    def __init__(self, name, latitude, longitude, food_type, has_wifi):
        # Call the parent (Restaurant) constructor
        super().__init__(name, latitude, longitude, food_type)
        # Store has_wifi as an attribute
        self.has_wifi = has_wifi
 
    # Override get_popup_text() to include wifi info
    def get_popup_text(self):
        wifi_bool = "Yes" if self.has_wifi else "No"
        return f"<b>CAFE: {self.name}</b><br>Food: {self.food_type}<br>WiFi: {wifi_bool}"
 
    # Override get_marker_color() — use "orange" for cafes
    def get_marker_color(self):
        return "orange"



class MyMap:
   
    
    def __init__(self, city, zoom=12):
        """Create a new map centered on a city"""
        self.city = city
        self.places = []  # List to store all our places
        
        # Map centers for some cities
        centers = {
            "Paris": [48.8566, 2.3522],
            "London": [51.5074, -0.1278],
            "New York": [40.7128, -74.0060],
            "Tokyo": [35.6762, 139.6503],
            "Vancouver": [49.2827, -123.1207]
        }
        
        # Get center coordinates or use default
        if city in centers:
            center = centers[city]
        else:
            center = [0, 0]  # Default to (0,0)
            print(f"Warning: {city} not in our list, using (0,0)")
        
        # Create the map
        self.map = folium.Map(location=center, zoom_start=zoom)
        print(f"🗺️  Created map of {city}")
        
        
    def add_place(self, place):
        
        # Add to our list
        self.places.append(place)
        
        # Create a marker on the map
        folium.Marker(
            location=[place.latitude, place.longitude],
            popup=place.get_popup_text(),  # Different for each place type!
            tooltip=place.name,
            icon=folium.Icon(color=place.get_marker_color())  # Different colors!
        ).add_to(self.map)
        
        print(f"  ✅ Added: {place.name}")
    
    def show_distances(self):
        
        if len(self.places) < 2:
            print("Add at least 2 places to see distances")
            return
        
        print(f"\n📏 Distances in {self.city}:")
        for i in range(len(self.places)):
            for j in range(i+1, len(self.places)):
                place1 = self.places[i]
                place2 = self.places[j]
                dist = place1.distance_to(place2)
                print(f"  {place1.name} → {place2.name}: {dist} km")
    
    def save(self, filename="my_map.html"):
        """Save the map to an HTML file"""
        self.map.save(filename)
        print(f"\n💾 Map saved as '{filename}'")
        return filename



def create_my_places():
    
    places = []
    
    #  Add at least 2 restaurants
    # Example: Restaurant("Pizza Hut", 40.7128, -74.0060, "Italian")
    # restaurants = [...]
    restaurants = [
        
        Restaurant("Le Parfait", 49.2827, -123.1207, "French"),
        Restaurant("Top Of Vancouver", 49.2835, -123.1187, "French")

    ]
    
    # Add at least 2 parks
    # parks = [...]
    parks = [
        Park("Stanley Park", 49.3043, -123.1443, True),
        Park("Queen Elizabeth Park", 49.2418, -123.1126, False)
    ]
    # Add at least 1 museum
    # museums = [...]
    museums = [
        Museum("Science World", 49.2734, -123.1038, "Science")
    ]

    cafes = [
        Cafe("Revolver Coffee", 49.2827, -123.1122, "Coffee", True)
    ]
    # Combine all places
    places.extend(restaurants)
    places.extend(parks)
    places.extend(museums)
    places.extend(cafes)
    
    return places


def find_closest_places(places):
    closest_place1 = places[0]
    closest_place2 = places[1]
    min_distance = closest_place1.distance_to(closest_place2)

    for i in range(len(places)):
        for j in range(i + 1, len(places)):
            dist = places[i].distance_to(places[j])
            if dist < min_distance:
                min_distance = dist
                closest_place1 = places[i]
                closest_place2 = places[j]

    print(f"\n📍 Closest pair: {closest_place1.name} & {closest_place2.name} ({min_distance} km apart)")
    return closest_place1, closest_place2


def parse_coordinates_from_link(link):
    """
    Pull latitude and longitude out of a Google Maps link.
 
    Google Maps links look like one of these:
      https://www.google.com/maps?q=49.2827,-123.1207
      https://www.google.com/maps/@49.2827,-123.1207,15z
      https://maps.google.com/?q=49.2827,-123.1207
 
    We look for the part after 'q=' or '@' and grab the two numbers.
    """
    # Try to find coordinates after "q="
    if "q=" in link:
        coords_part = link.split("q=")[1]      # grab everything after "q="
        coords_part = coords_part.split("&")[0]  # remove anything after "&" if present
    # Try to find coordinates after "@"
    elif "@" in link:
        coords_part = link.split("@")[1]        # grab everything after "@"
    else:
        print("❌ Could not find coordinates in that link.")
        print("   Make sure it looks like: https://www.google.com/maps?q=49.2827,-123.1207")
        return None, None
 
    # Split "49.2827,-123.1207" into ["49.2827", "-123.1207"]
    parts = coords_part.split(",")
 
    # Convert strings to float numbers
    latitude = float(parts[0])
    longitude = float(parts[1])
 
    return latitude, longitude
 
 
def add_place_from_link(mymap, filename="my_favorite_places.html"):
   
    print("\n" + "=" * 50)
    print("📌 ADD A NEW PLACE FROM GOOGLE MAPS")
    print("=" * 50)
    print("How to get a link:")
    print("  1. Open Google Maps in your browser")
    print("  2. Right-click any spot on the map")
    print("  3. Click the coordinates shown at the top")
    print("  4. Paste them here as: https://www.google.com/maps?q=LAT,LON")
    print("-" * 50)
 
    # Step 1 — get the link from the user
    link = input("\n🔗 Paste your Google Maps link: ").strip()
 
    # Step 2 — parse coordinates out of the link
    latitude, longitude = parse_coordinates_from_link(link)
    if latitude is None:
        return  # something went wrong, message already printed inside parse
 
    print(f"✅ Found coordinates: {latitude}, {longitude}")
 
    # Step 3 — ask what type of place it is
    print("\nWhat type of place is this?")
    print("  1 — Restaurant")
    print("  2 — Park")
    print("  3 — Museum")
    print("  4 — Cafe")
    place_type = input("Enter number (1/2/3/4): ").strip()
 
    # Step 4 — ask for the name
    place_name = input("📝 Name of the place: ").strip()
 
    # Step 5 — create the right object based on type chosen
    if place_type == "1":
        food_type = input("🍽️  Food type (e.g. Italian, French): ").strip()
        new_place = Restaurant(place_name, latitude, longitude, food_type)
 
    elif place_type == "2":
        has_playground_input = input("🛝  Has playground? (yes/no): ").strip().lower()
        has_playground = True if has_playground_input == "yes" else False
        new_place = Park(place_name, latitude, longitude, has_playground)
 
    elif place_type == "3":
        entry_fee = input("🎟️  Entry fee (e.g. 15): ").strip()
        new_place = Museum(place_name, latitude, longitude, entry_fee)
 
    elif place_type == "4":
        food_type = input("🍽️  Food type (e.g. Coffee, Brunch): ").strip()
        has_wifi_input = input("📶  Has WiFi? (yes/no): ").strip().lower()
        has_wifi = True if has_wifi_input == "yes" else False
        new_place = Cafe(place_name, latitude, longitude, food_type, has_wifi)
 
    else:
        print("❌ Invalid choice, place not added.")
        return
 
    # Step 6 — add the new place to the map
    mymap.add_place(new_place)
 
    # Step 7 — re-save the map so the new marker appears in the file
    mymap.save(filename)
    print(f"\n🌐 Map updated! Open '{filename}' in your browser to see the new marker.")

def main():
    
    print("=" * 50)
    print("🗺️  MY FAVORITE PLACES MAP")
    print("=" * 50)
    print("\nThis program demonstrates the 4 pillars of OOP:")
    print("1. ENCAPSULATION: Place class bundles data + methods")
    print("2. INHERITANCE: Restaurant, Park, Museum inherit from Place")
    print("3. POLYMORPHISM: get_popup_text() works differently for each")
    print("4. ABSTRACTION: MyMap hides map complexity")
    print("\n" + "-" * 50)
    
    #  Choose a city
    # Available: Paris, London, New York, Tokyo
    my_city = "Vancouver"  # Change this to your favorite city
    
    # Create a map
    mymap = MyMap(my_city)
    
     
    #my_places = create_my_places()
    
    # For now, let's use some sample places (replace with your own!)
    print("\n📝 Using sample places (TODO: Replace with your favorites!)")
    
    # Create some sample places
    sience_world = Museum("Science World", 49.2734, -123.1038, "Science")
    restaurant = Restaurant("Top Of Vancouver", 49.2835, -123.1187, "French")
    park = Park("Queen Elizabeth Park", 49.2418, -123.1126, True)
    cafe = Cafe("Revolver Coffee", 49.2827, -123.1122, "Coffee", True)
    
    # Add all places to the map
    mymap.add_place(sience_world)
    mymap.add_place(restaurant)
    mymap.add_place(park)
    mymap.add_place(cafe)
    
    # Show distances between places
    mymap.show_distances()

    find_closest_places([sience_world, restaurant, park, cafe])
    
    # Save the map
    filename = mymap.save("my_favorite_places.html")
    
    # Open in browser
    print("\n🌐 Opening map in browser...")
    webbrowser.open(filename)
    
    print("\n" + "=" * 50)
    print("✅ EXERCISE COMPLETE!")
    print("=" * 50)
    print("\nREFLECTION QUESTIONS:")
    print("1. How did Restaurant, Park, and Museum INHERIT from Place?")
    print("2. How is POLYMORPHISM shown when adding places to the map?")
    print("3. What data and methods are ENCAPSULATED in the Place class?")
    print("4. What complexity does the MyMap class ABSTRACT away?")
    print("\n🎯 BONUS: Try adding your own real favorite places!")

    print("\n" + "-" * 50)
    want_to_add = input("➕ Want to add a new place from a Google Maps link? (yes/no): ").strip().lower()
    if want_to_add == "yes":
        add_place_from_link(mymap, filename)



if __name__ == "__main__":
    main()