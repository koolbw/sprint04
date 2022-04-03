from multiprocessing.spawn import old_main_modules
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def initializeFirestore():

   # Initialize database
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "sprint04-4a465-firebase-adminsdk-luj65-0ab2807726.json"
   cred = credentials.ApplicationDefault()
   firebase_admin.initialize_app(cred, {
      'projectId': 'sprint04-4a465',
   })

   db = firestore.client()

   return db

def printMenu():
   print("\n--MAIN MENU--")
   print("1. View Recipes")
   print("2. Add Recipe")
   print("3. Remove Recipe")
   print("4. Exit")

def viewRecipes():
   results = db.collection("recipes").get()
   print("\nRecipes: ")
   print(f"-->{'Name':<15}-->{'Ingredients':<35}-->{'Instructions':<55}-->{'Cook Time':<10}\n")
   for result in results:
      item = result.to_dict()
      print(f"-->{result.id:<15}-->{str(item['ingredients']):<35}-->{str(item['instructions']):<55}-->{item['cookTime']:<10}")



def addRecipe(db):
   name = input("Recipe Name: ")
   ingredients = input("Ingredients: ")
   instructions = input("Instructions: ")
   cookTime = int(input("Cook time(min): "))

   result = db.collection("recipes").document(name).get()
   if result.exists:
      print("Recipe already exists.")
      return

   data = {"name" : name, 
           "ingredients" : ingredients,
           "instructions" : instructions,
           "cookTime" : cookTime}

   db.collection("recipes").document(name).set(data)

   log_transaction(db, f"Added recipe for {name}")
   print(f"Added recipe for {name}! ")

   # doc_ref = db.collection(u'recipes').document(u'tacos')
   # doc_ref.set({
   #    u'name': u'Tacos',
   #    u'ingredients': u'tortillas, meat, cheese',
   #    u'instructions': "Lots of things to do.",
   #    u'prepTime': 45
   # })
   # print("addingRecipe")

def removeRecipe(db):
   name = input("Which recipe would you like to remove? ")
   
   result = db.collection("recipes").document(name).get()
   if not result.exists:
      print("That recipe does not exist. ")
      return
   
   confirmation = input(f"Are you sure you want to remove the recipe for {name}? (y/n) ")
   if confirmation == "y":
      db.collection("recipes").document(name).delete()
      log_transaction(db, f"Recipe for {name} was removed")
      print("Recipe removed! ")
   else:
      return


def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)


running = True
db = initializeFirestore()
while running:
   printMenu()
   choice = int(input("--> "))

   if choice == 1:
      viewRecipes()
   elif choice == 2:
      addRecipe(db)
   elif choice == 3:
      removeRecipe(db)
   elif choice == 4:
      print("\nThank you, See you soon!")
      running = False
      break
   else:
      print("\nInvalid input. Try again.")
