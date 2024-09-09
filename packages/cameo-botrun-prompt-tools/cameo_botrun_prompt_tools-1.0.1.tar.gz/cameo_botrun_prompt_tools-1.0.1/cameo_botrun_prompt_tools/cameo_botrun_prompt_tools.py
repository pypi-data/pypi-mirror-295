def print_button(button_name, button_prompt):
    button_txt = f'@begin button(\"{button_name}\") {button_prompt} @end'
    print(button_txt)

def print_link(url, link_prompt):
    link_txt = f'@begin link(\"{url}\") {link_prompt} @end'
    print(link_txt)
