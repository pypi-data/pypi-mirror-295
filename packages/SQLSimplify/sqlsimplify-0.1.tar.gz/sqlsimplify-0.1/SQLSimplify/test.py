import quicksql

db = quicksql.Connect('localhost','root',"1",'wp')

db.get.columns('wp_options')
