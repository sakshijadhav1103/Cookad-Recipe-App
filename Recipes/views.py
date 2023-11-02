from django.shortcuts import render,reverse, redirect
from . import models
import requests
from django.conf import settings
from .mixins import (
	FormErrors,
	RedirectParams,
	APIMixin
)

# Create your views here.
def home(request):
    recipes=models.Recipe.objects.all()
    context={'recipes':recipes}
    return render(request,'Recipes/home.html',context)

def about(request):
    return render(request,'Recipes/about.html',{'title':"about us page"})

def index(request):
    if request.method == "POST":
        cat = request.POST.get("cat", None)
        query = request.POST.get("query", None)

        if not cat or not query:  # If category or query is not provided, render home page with an error message
            return render(request, 'recipes/home.html', {'error': 'Please select a category and provide a search query.'})

        return RedirectParams(url='Recipes:results', params={"cat": cat, "query": query})

    # If no category or query provided, render home page with an error message
    return render(request, 'recipes/home.html', {'error': 'Please provide a valid category and search query.'})

'''
Basic view for displaying results
'''
def results(request):

	cat = request.GET.get("cat", None)
	query = request.GET.get("query", None)

	if cat and query:
		results = APIMixin(cat=cat, query=query).get_data()

		if results:
			context = {
				"results": results,
				"cat": cat,
				"query": query,
			}

			return render(request, 'recipes/results.html', context)
	
	return redirect(reverse('Recipes:home'))


def recipe_detail(request, recipe_id):
    # API endpoints
    instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    information_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

    # Fetch recipe instructions
    instructions_response = requests.get(instructions_url, params={'apiKey': settings.API_KEY})
    instructions_data = instructions_response.json() if instructions_response.ok else None

    # Fetch recipe information
    information_response = requests.get(information_url, params={'apiKey': settings.API_KEY})
    information_data = information_response.json() if information_response.ok else None

    if instructions_data and information_data:
        # Extract relevant information
        instructions = instructions_data[0].get('steps', []) if instructions_data else []
        ingredients = information_data.get('extendedIngredients', [])

        context = {
            'instructions': instructions,
            'ingredients': ingredients,
        }
        return render(request, 'recipes/recipe_detail.html', context)
    else:
        return render(request, 'recipes/error.html')


def substitutes(request):
    if request.method == "GET":
        ingredient = request.GET.get("ingredient", None)
        
        if not ingredient:
            return render(request, 'Recipes/substitute.html', {'error': 'Please provide an ingredient for substitution.'})

        substitutes_url = f"https://api.spoonacular.com/food/ingredients/substitutes"

        substitutes_response = requests.get(substitutes_url, params={'apiKey': settings.API_KEY, 'ingredientName': ingredient})
        substitutes_data = substitutes_response.json() if substitutes_response.ok else None

        if substitutes_data and 'substitutes' in substitutes_data:
            context = {
                "substitutes": substitutes_data['substitutes'],
                "ingredient": substitutes_data['ingredient'],
            }

            return render(request, 'Recipes/substitute.html', context)

        return render(request, 'Recipes/substitute.html', {'error': 'No substitutes found for the provided ingredient.'})

    return redirect(reverse('Recipes:home'))


def conversions(request):
    if request.method == "GET":
        ingredient = request.GET.get("ingredientName", None)
        source_amount = request.GET.get("sourceAmount", None)
        source_unit = request.GET.get("sourceUnit", None)
        target_unit = request.GET.get("targetUnit", None)

        if not ingredient or not source_amount or not source_unit or not target_unit:
            return render(request, 'Recipes/conversion.html', {'error': 'Please provide all conversion parameters.'})

        conversions_url = f"https://api.spoonacular.com/recipes/convert"

        conversions_response = requests.get(conversions_url, params={'apiKey': settings.API_KEY, 'ingredientName': ingredient, 'sourceAmount': source_amount, 'sourceUnit': source_unit, 'targetUnit': target_unit})
        conversions_data = conversions_response.json() if conversions_response.ok else None

        if conversions_data:
            context = {
                "conversions": conversions_data,
                "ingredient": ingredient,
                "source_amount": source_amount,
                "source_unit": source_unit,
                "target_unit": target_unit,
            }

            return render(request, 'Recipes/conversion.html', context)

        return render(request, 'Recipes/conversion.html', {'error': 'Conversion not found for the provided input.'})

    return redirect(reverse('Recipes:home'))



