# SmartPlate
SmartPlate is a Python-based application that implements fractional knapsack using greedy methods.

It optimizes a meal selection while maintaining the imposed calorie constraint of the user.

Based on a study by Seljak (2004) which used single-objective multi-constrained fractional knapsack to compose balanced and healthy meals. 

# How to use
## Option 1
You can just run the exe file when you download the zip or clone the repository

## Option 2
You can use the installer to directly download the files and run the exe

## Option 3
Run it in the terminal

but to do it you have to create a .env file with the api key and api id acquired from nutritionix

the file should look like this:
```env
api_key={your api key}
api_id={your api id}
```

You also need to pip install these libraries:
```bash
pip install python-dotenv
pip install request
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
