# googolplex-pdf-search
Python program for searching pdf text, ranking the results and exporting highlighted search results in pdf. Uses trie structure, stack, heap, page graph. Converts queries to postfix notation. Allows for logical expressions and phrases. Offers did you mean functionality.

## Required libraries
- PyMuPDF
- didyoumean.py

## How to install and run the program

1. Create a virtual environment in the project directory:
```virtualenv venv```
2. Activate the virtual environment:

    2.1. For Windows:
```venv\Scripts\activate```

    2.2. For Linux:
```source venv/bin/activate```
3. Install the required libraries:
```pip install -r requirements.txt```
4. Run the program:
```python main.py```
5. All in one command:

    5.1. For linux
   ```virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py```

    5.1. For windows
```virtualenv venv && venv\Scripts\activate && pip install -r requirements.txt && python main.py```

## Application screenshots

<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173469590-357ebc6b-b0ca-4c3b-963d-bec9cd4d6dc7.png" />
  <p align="center">Ilustration 1 - Loading bar.</p>
</div>


<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173468613-f2f6bb18-5223-451e-af30-8d871cf65e85.png" />
  <p align="center">Ilustration 2 - Autocomplete feature.</p>
</div>

<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173472886-1813ea3c-9586-4493-96a9-dc35c05c9af1.png" />
  <p align="center">Ilustration 3 - Did you mean functionality.</p>
</div>

<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173468848-4131545b-40a8-421a-9fa1-3f89857bb679.png" />
  <p align="center">Ilustration 4 - Third page of results for the search query graph.</p>
</div>

<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173469035-59f6df96-20f0-4589-bed3-3994fbd2f9eb.png" />
  <p align="center">Ilustration 5 - Complex logical query with OR, AND and grouping with brackets.</p>
</div>

<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173469726-42ab96b6-4e57-43d1-b01c-c83c5faa0347.png" />
  <p align="center">Ilustration 6 - Complex logical query with negation (NOT) and grouping with brackets.</p>
</div>


<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173472600-e7f8c197-b63f-4b48-a34f-17cb6dd86d47.png" />
  <p align="center">Ilustration 7 - Phrase search for "skip list" by using the double quotes.</p>
</div>


<div align="center">
<img alt="signal-visualization" align="center" width="100%" src="https://user-images.githubusercontent.com/34657562/173472562-6d656436-4575-48df-bc06-58c551ec9314.png" />
  <p align="center">Ilustration 8 - Generated pdf with highlighted search query "skip list".</p>
</div>




