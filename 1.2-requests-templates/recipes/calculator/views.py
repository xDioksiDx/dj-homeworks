from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def recipe_view(request, dish):
    servings_str = request.GET.get("servings")

    try:
        servings = int(servings_str) if servings_str is not None else 1
    except ValueError:
        servings = 1

    if servings <= 0:
        servings = 1

    recipe_data = DATA.get(dish, {})  # если рецепта нет, будет пустой словарь
    recipe = {name: amount * servings for name, amount in recipe_data.items()}

    context = {"recipe": recipe}
    return render(request, "calculator/recipe.html", context)