from __future__ import annotations
import random



class sText:

    def __init__(self,text:str):
        self.text:str=text

    def __str__(self):
        return self.text

    def __eq__(self,other):
        return self.text==other.text if isinstance(other,sText) else self.text==other

    def __ne__(self,other):
        return self.text!=other.text if isinstance(other,sText) else self.text!=other

    def __add__(self,other):
        if isinstance(other,sText): return f"{self.text}{other.text}"
        elif isinstance(other,str): return f"{self.text}{other}"
        else: raise TypeError(f"Can only add objects of type Text or str, not {type(other)}.")

    def __radd__(self,other):
        if isinstance(other,sText): return f"{other.text}{self.text}"
        elif isinstance(other,str): return f"{other}{self.text}"
        else: raise TypeError(f"Can only add objects of type Text or str, not {type(other)}.")

    def encrypt(self,use_rich:bool=True)->sText:
        """Creates a string that's just gibberish (example: *??#&&#*#%%?#) optionally in different colors (if use_rich=True).
        You can optionally give a string that guarantees that the returned gibberish will be the length of that given string.

        Args:
            use_rich (bool, optional): Whether the string should be in different colors or not. Warning: if you don't use rich in your code and this is set to True, the encrypted version is going to be very ugly. Defaults to True.

        Returns:
            Text: The gibberish.
        """
        characters="#$%&*?@"
        colors=[
            "red","green","yellow","blue","magenta","cyan",
            "bright_red","bright_green","bright_yellow","bright_blue","bright_magenta","bright_cyan"
        ]

        prev_chars:list=[]
        converted_characters="".join(
            random.choice(characters) if char!=" " else " "
            for char in (self.text or "".join(random.choice(characters) for _ in range(random.randint(7,14))))
            if char==" " or (random.choice([x for x in characters if x not in prev_chars]) not in prev_chars and (prev_chars.append(char) or True) and (len(prev_chars)<=2 or prev_chars.pop(0)))
        )

        if not use_rich:
            return sText(converted_characters)

        prev_color=""
        def get_forbidden_color(color:str)->str:
            if color=="":
                return ""
            return color.replace("bright_","") if color.startswith("bright_") else "bright_"+color

        styled_text=""
        for char in converted_characters:
            forbidden_color:str=get_forbidden_color(prev_color)
            available_colors:list[str]=[c for c in colors if c!=prev_color and c!=forbidden_color]
            new_color:str=random.choice(available_colors)
            styled_text+=f"[{new_color}]{char}[/]"
            prev_color:str=new_color

        return sText(styled_text)