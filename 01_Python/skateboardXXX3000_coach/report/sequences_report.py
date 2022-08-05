import jinja2
import os


latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('./'))
)
template = latex_jinja_env.get_template('test.tex')
render = template.render(section1='Long Form', section2='Short Form')

with open("render_test.tex","w") as f:
    f.write(render)