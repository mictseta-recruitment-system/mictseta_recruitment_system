from django.core.management import call_command

def my_backup(filename):
	try:
		call_command('dbbackup', output_filename=filename)
	except:
		pass


def my_restore(filename):
	try:
		call_command(f"dbrestore -i '{filename}'")
	except:
		print(f"No such file '{filename}'")