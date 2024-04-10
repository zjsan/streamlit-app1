
#testing program for optimized prompts in question generation according to bloom
#need to import natural language processing tools for the training of datas
#get response from the llm and test it to the trained data 
#if mapping of bloom's levels with the response is done and accurate
#then return response to the llm for further processing
blooms_taxonomy = {'Remembering': ['recognizing', 'identifying','recalling'],'Understand': ['interpreting', 'clarifying', 'paraphrasing ', 'representing','translating', 'illustrating', 'classifying', 'categorizing', 'summarizing','concluding','interpolating', 'predicting','comparing','explaining'], 
    'Apply': ['executing', 'carrying out','implementing', 'using'], 'Analyze': ['differentiating', 'discriminating', 'distinguishing', 'focusing','selecting','organizing','finding coherence','integrating','outlining',
        'parsing', 'structuring',' attributing', 'deconstructing'], 'Evaluate':['checking', 'coordinating','detecting','monitoring','testing','critiquing','judging'],'Create': ['generating','hypothesizing','planning','designing','producing','construct']}



for x,y in blooms_taxonomy.items():
    print(x,y)
print(blooms_taxonomy.get('Remembering'))