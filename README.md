# COMPAS-LCA

COMPAS-LCA is a modular software package that trials an LLM-based IFC-LCA workflow. 

User-Manual:
1. Install dependencies. They can be found in the requirements.txt. Depending on which LLM you want to use, you must also install the corresponding packages.
2. Drag and drop your IFC file into data/input/IFC_model. Note: COMPAS-LCA only supports IFC models of schema 2x3
3. Specify the configurations in the master config file (config/master_config.yaml). Here all user-defined configurations, such as choosing the LCA database, choosing the LLM provider and inserting the API key, specifying modular prompt instructions, and customizing the IFC data input for the LLM-based matching module can be found. Detailed instructions are provided within the file.
4. When you are content with the configuration settings, you can run the first module (extraction module). Depending on the file size, the amount of elements geometries in the IFC file the complextiy of the geometries if brep_toggle is "True" within the master_config, this module might take a long time (i.e., a couple of hours).
5. After running the first module, you will have access to metadata and a preliminary bill of quantities of the IFC model. Depending on the chosen provider, a cost estimation will be presented. As a benchmark: running gpt-4o costs approximately 0.01 cents (so if the amount of unique inferences is 200, then the entire LLM-based matching will cost 2 dollars). Furthermore, prompt and models settings can be still adjusted in the master_config.yaml, before proceeding with the second module. Also, module 01d_filter_data can be run again, if you wish to customize the input IFC data for the LLM, and further minimize tokens. The filtering instructions (and recommendations) are listed more thoroughly in the master_config.yaml in section "filter_config".




The "master_config_template.yaml" filename needs to be changed to "master_config.yaml". Change due to sensitive "API key" and adjusted in .gitignore


Upload ONE IFC file into the the folder data/input/IFC_model
Insert the LLM model specs and API key into the "master_config.yaml"
Check the "master_config.yaml", specify the inputs (or leave default)
