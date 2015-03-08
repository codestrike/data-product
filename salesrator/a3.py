class cleanup_dict:
	operations=[
	    {'operation' : 'data_types', 'id' : '100' , 'para' :[]},
	    {'operation' : 'describe_numeric', 'id' : '101' , 'para' :[]},
	    {'operation' : 'describe_all', 'id' : '102' , 'para' :[]},
	    {'operation' : 'describe_categorical', 'id' : '103' , 'para' :[]},
	    {'operation' : 'get_unique_vals', 'id' : '104' , 'para' :[]},
	    {'operation' : 'num_outliers', 'id' : '105' , 'para' :[]},
	    {'operation' : 'missing_value', 'id' : '106' , 'para' :['cols' , 'replace_by']},
	    {'operation' : 'replace_value', 'id' : '107' , 'para' :['to_replace' , 'col' , 'replace_by']},
	    {'operation' : 'replace_non_number', 'id' : '108' , 'para' :['cols' , 'replace_by']},
	    {'operation' : 'replace_negative', 'id' : '109' , 'para' :['col' , 'delete' , 'replace_by']},
	    {'operation' : 'to_upper', 'id' : '1010' , 'para' :['col']},
	    {'operation' : 'to_lower', 'id' : '1011' , 'para' :['col']},
	    {'operation' : 'strip_left_right', 'id' : '1012' , 'para' :['col']},
	    {'operation' : 'slice_string', 'id' : '1013' , 'para' :['col' , 'number']},
	    {'operation' : 'floor', 'id' : '1014' , 'para' :['col','floor','delete','replace_by']},
	    {'operation' : 'cap', 'id' : '1015' , 'para' :['col','cap','delete','replace_by']},
	    {'operation' : 'convert_to_float', 'id' : '1016' , 'para' :['cols']},
	    {'operation' : 'convert_to_int', 'id' : '1017' , 'para' :['cols']},
	    {'operation' : 'string_to_float', 'id' : '1018' , 'para' :['cols']},
	    {'operation' : 'convert_to_category', 'id' : '1019' , 'para' :['cols']},
	    {'operation' : 'string_to_int', 'id' : '1020' , 'para' :['cols']},
	    {'operation' : 'remove_lower_outlier', 'id' : '1021' , 'para' :['col','lower']},
	    {'operation' : 'remove_higher_outlier', 'id' : '1022' , 'para' :['col','higher']},
	    {'operation' : 'delete_col', 'id' : '1023' , 'para' :['group_cols']}
	    ]
	   