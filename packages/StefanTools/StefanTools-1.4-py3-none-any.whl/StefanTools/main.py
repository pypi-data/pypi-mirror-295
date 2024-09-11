import json
from inputimeout import inputimeout
import sys
import time
import string
import re
import inflect
import typing
import os
import inspect



from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.text import Text as rich_Text
from rich.style import Style
install()
theme={"success":"bold green","failure":"bold red","warning":"bold red","celebrate":"bold yellow","debug":"bold blue",\
"info":"bold white","question":"bold magenta"}
my_theme=Theme(theme)
console=Console(theme=my_theme)



from .methods import exclusive



limit=1.7976931348623157*(10**308)



class input:

    """Contains functions like *int* or *float*.
    They try to input their assigned type from the user continuously until they get it.
    """

    @staticmethod
    def int(*args,**kwargs)->int: return input.main_loop(type_=int,*args,**kwargs)

    @staticmethod
    def float(*args,**kwargs)->float: return input.main_loop(type_=float,*args,**kwargs)

    @exclusive.file
    @staticmethod
    def main_loop(
            type_:type,
            msg:str="", print_msg_on_every_try:bool=False,
            catch:bool=True, text_on_error:str="Please enter a number. ({e})"
        ):
        msg=format.text.end(msg,add=": ")
        console.print(msg,style="question",end="")
        while True:
            a=None
            if catch:
                try:
                    if print_msg_on_every_try:
                        console.print(msg,style="question",end="")
                    a=inputimeout(timeout=limit)
                    a=type_(a)
                except (ValueError,TimeoutError) as e:
                    console.print(text_on_error.replace("{e}",str(e)),style="failure")
                    continue
            else:
                a=inputimeout(timeout=limit)
                a=type_(a)
            return a



class output:

    @staticmethod
    def normal(*args,**kwargs)->None:
        output.output(use_rich=False,*args,**kwargs)

    @staticmethod
    def rich(*args,**kwargs)->None:
        output.output(use_rich=True,*args,**kwargs)

    @exclusive.dir
    @staticmethod
    def output(text:typing.Any="",style:str="",end:str="\n",sep:str=" ",animation:bool=True,delay:float=0.01,use_rich:bool=True,\
delay_between_lines:float=0.0,auto_color:dict[str,str]={})->None:

        """Just prints text.

        Args:
            text (Any, optional): The text to print. If it's a list, it will be treated as if you put a comma between elements in a normal print() statement. If it's neither a list or a string, it will be turned to a string using str(text). Defaults to "".
            style (str, optional): The style to use. Has no use if use_rich is set to False. Defaults to "".
            end (str, optional): The thing to put at the end of the text. Defaults to a new line.
            sep (str, optional): The thing that is printed between each element of the list. Is useless if text is not a list or is a list with 1 element. Defaults to " ".
            animation (bool, optional): Whether to animate the printing of the text. Defaults to True.
            delay (float, optional): The delay between printing characters. Defaults to 0.01.
            use_rich (bool, optional): Whether to use rich. Defaults to True.
            delay_between_lines (float, optional): The delay between printing elements of the list text. Is useless if text is not a list or is a list with 1 element. Defaults to 0.0.
            auto_color (dict, optional): A dictionary of words to look out for and if they are in the word, color them. \
    **This may color parts of a word you maybe didn't want it to color. \
    To fix that, instead of setting the value of auto_color to {"a","red"}, instead, set it to {" a ","red"}.** Defaults to {}.

        Returns:
            None (None): Nothing.

        """


        if isinstance(text,str):
            text=[text]
        if isinstance(text,dict):
            old_text=text
            text=[]
            x=0
            for key,value in old_text.items():
                text[x]=f"{key}: {value}"
                x+=1
            del old_text
        elif not isinstance(text,list):
            text=[str(text)]


        global theme
        if style in theme:
            style=theme[style]
        style=style if use_rich else ""

        for try_to_find,color in auto_color.items():
            for x in range(len(text)):
                text[x]=re.sub(rf"({try_to_find})",rf"[{color}]\1[/]",text[x],flags=re.IGNORECASE)

        def one_line(line:str)->None:

            if animation:


                if use_rich:
                    rich_text=rich_Text.from_markup(line)
                    segments=rich_text.render(console)

                    for segment in segments:
                        segment_text=segment.text
                        style_a:Style=Style.parse(style)
                        if segment.style is None:
                            segment_style:Style=style_a
                        else:
                            segment_style:Style=style_a+segment.style #Don't change the order that these 2 are being added, it's important
                        for letter in segment_text:
                            console.print(rich_Text(letter,style=segment_style),end="")
                            time.sleep(delay)
                else:
                    for letter in line:
                        print(letter,end="",flush=True)
                        time.sleep(delay)


            else:
                if use_rich:
                    console.print(line,style=style,end="")
                else:
                    print(line,end="")

            time.sleep(delay_between_lines)


        if not isinstance(text,dict):
            for line in text:
                one_line(line)
                if sep!="" and len(text)>1:
                    output.output(sep,animation=animation,style=style,end="",sep="")
            if end!="":
                output.output(end,animation=animation,style=style,end="")
        else:
            console.print(text,style=style)



class data:


    @staticmethod
    def save(data:typing.Any,save_location:str,spaces:int=4)->None:
        """Takes data and writes it to a .json file.

        Args:
            data (Any): The data to save.
            save_location (str): The directory of the .json file.
            spaces (int, optional): In the .json file, how much spaces to indent things. Defaults to 4.

        Raises:
            ValueError: If the save_location variable doesn't end with ".json".
        """
        if not save_location.endswith(".json"):
            raise ValueError("save_location must end with \".json\"")
        with open(save_location,"w") as json_file:
            json.dump(data,json_file,indent=spaces)


    @staticmethod
    def load(file_location:str)->typing.Any:
        """Reads data from a .json file.

        Args:
            save_location (str): The directory of the .json file.

        Returns:
            Any: The data that was read in the .json file.
        """
        if not file_location.endswith(".json"):
            raise ValueError("save_location must end with \".json\"")
        with open(file_location,"r") as json_file:
            data=json.load(json_file)
        return data



class format:


    class number:

        @staticmethod
        def scientific_notation(n:int,return_the_plus:bool=True,decimals:int=2,lower_limit:int=0)->str|int:
            """Formats a number as scientific notation (example: 1500000 -> 1.5e6) and returns it as a string.

            Args:
                n (int): The number to format.
                return_the_plus (bool, optional): If n=1500000, will the function return 1.5e+6 (return_the_plus=True) or 1.5e6 (return_the_plus=False). Defaults to True.
                decimals (int, optional): If n=1234567, will the function return 1.12e6 (decimals=2) or 1.123457e6 (decimals=6). Defaults to 2.
                lower_limit (int, optional): If n is smaller than this number, the function will return the string version of n.

            Returns:
                str: The formatted number.
            """

            if n>=lower_limit:
                returns=f"{n:.{decimals}e}"
                if not return_the_plus:
                    return returns.replace("+","")
                return returns
            else:
                return str(n)

        @staticmethod
        def text(number:typing.Union[int,str],ordinal:bool=False)->str:
            """Returns the number in its text form (example: 1 -> one/first).

            Args:
                number (int or str): The number to be converted.
                ordinal (bool, optional): Does the program return an ordinal number (examples of ordinal numbers: first, second, third) or not. Defaults to False.

            Returns:
                str: The number in a word form.
            """
            number=int(number)
            p=inflect.engine()
            if ordinal: return p.ordinal(number) #type:ignore is necessary
            else:       return p.number_to_words(number) #type:ignore is necessary


    class text:

        @staticmethod
        def end(msg:str,add:str):

            for i in range(min(len(msg),len(add))): #max_overlap=min(len(msg),len(add))
                if msg.endswith(add[:i+1]):
                    return msg+add[i+1:]

            return msg+add







def clear(method:int=1):
    if method==1 and not isinstance(method,bool): #The "not isinstance(method,bool)" prevents True or False getting in the if block
        sys.stdout.flush()
        time.sleep(0.1)
        print("\033[2J\033[H",end="",flush=True)
        time.sleep(0.1)
        sys.stdout.flush()
    elif method==2:
        print("\033c",end="",flush=True)
    #both of the methods are copied from https://ask.replit.com/t/clear-console-in-python/65265
    elif method==0 and not isinstance(method,bool):
        raise ValueError(f"Invalid method 0. In the 1.2 update, the method 0 was removed. Please use method 1 instead.")
    else:
        raise ValueError(f"Invalid method {method}.")



class words:


    @exclusive.file
    @staticmethod
    def get_final_list(initial_list:list[str])->list[str]:

        @exclusive.file
        def apply_transformations(element:str)->list[str]:
            variations=set([element])

            @exclusive.file
            def remove_apostrophe(s:str)->str:
                return s.replace("'","")
            @exclusive.file
            def capitalize_i(s:str)->str:
                return s.replace(" i "," I ")
            @exclusive.file
            def de_capitalize_i(s:str)->str:
                return s.replace(" I "," i ")
            @exclusive.file
            def to_upper(s:str)->str:
                return s.upper()
            @exclusive.file
            def to_lower(s:str)->str:
                return s.lower()
            @exclusive.file
            def cap_letters(s:str)->str:
                return string.capwords(s)

            def some_function_a(s:str):
                for transform in [remove_apostrophe,capitalize_i,de_capitalize_i,to_upper,to_lower,cap_letters]:
                    transformed=transform(s)
                    if transformed!=s: #It's only going to be added if there's an actual change
                        if transformed not in variations:
                            variations.add(transformed)
                            some_function_a(transformed)

            some_function_a(element)

            final_variations=set(variations)

            for variation in variations:
                for a in ["!","?",".","!?","?!"]:
                    final_variations.add(variation+a)

            return list(final_variations)

        final_list=[]
        for element in initial_list:
            final_list.extend(apply_transformations(element))
        final_list=list(dict.fromkeys(final_list))
        return final_list


    @staticmethod
    def positive()->list:
        initial_list=["y","yes","true","i would","indeed","ofc","of course","yes of course","i guess","ig","i should",\
"i guess i would","i think i should","yes indeed","i guess i should","why not"]
        return words.get_final_list(initial_list)


    @staticmethod
    def negative()->list:
        initial_list=["n","no","false","i wouldn't","no way","not at all","nope","no thanks","i don't","i guess not","no i don't",\
"ofc not"]
        return words.get_final_list(initial_list)


    @staticmethod
    def exit()->list:
        initial_list=["exit","exit program","quit","quit program","leave","leave program","abort","abort program","home","let me out",\
"lemme out","i wanna go","i want to go","let me leave"]
        return words.get_final_list(initial_list)


    @staticmethod
    def hurry()->list:
        initial_list=["hurry","hurry up","hurry up already"]
        return words.get_final_list(initial_list)



def fraction(first_number:int|float,second_number:int|float,multiply_by:int|float=1.0)->float:
    """Makes a fraction and returns it multiplied by an optional number.

    Args:
        first_number (int or float): The numerator (number in a fraction that's above).
        second_number (int or float): The denominator (number in a fraction that's below).
        multiply_by (int or float, optional): Multiply the result by this number. Defaults to 1.0.

    Returns:
        float: The first_number divided by second_number multiplied by multiply_by.
    """

    if isinstance(first_number,str) and first_number.isdigit():
        console.print(f"The numerator number {first_number} is a string. It has been turned into an integer.")
        first_number=int(first_number)
    if isinstance(second_number,str) and second_number.isdigit():
        console.print(f"The denominator number {second_number} is a string. It has been turned into an integer.")
        second_number=int(second_number)

    return (first_number/second_number)*multiply_by



class dir:

    @staticmethod
    def get()->str:
        caller_frame:inspect.FrameInfo=inspect.stack()[1]
        caller_filename:str=caller_frame.filename
        directory:str=os.path.dirname(os.path.abspath(caller_filename))
        return directory[0].upper()+directory[1:] if os.name=="nt" else directory



if __name__=="__main__":
    while True:
        #print(input.int("Input something "))
        #print("\n"*5)
        #console.print(Text.unknown())
        #print("\n"*5)
        #a=words.negative()
        #del a

        a=inputimeout(timeout=limit) #To avoid spamming the console.
        del a