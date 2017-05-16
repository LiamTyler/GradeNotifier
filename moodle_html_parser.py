from html.parser import HTMLParser

class Form:
    def __init__(self):
        self.name = ""
        self.action = ""
        self.inputs = []

class FormHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.forms = []
        self.current_form = None
        
    def handle_starttag(self, tag, attrs):
        if tag == "form":
            self.current_form = Form()
            for name, val in attrs:
                if name == "name":
                    self.current_form.name = name
                elif name == "action":
                    self.current_form.action = val
        elif tag == "input":
            tmp = {}
            for name, val in attrs:
                tmp[name] = val
            self.current_form.inputs.append(tmp)

    def handle_endtag(self, tag):
        if tag == "form":
            self.forms.append(self.current_form)


class MoodleGradeParser(HTMLParser):
    def __init__(self, inputfile=None, outputfile=None):
        HTMLParser.__init__(self)
        self.rawhtml = None
        self.course = False
        self.grade = False
        self.cur_link = None
        self.links = []
        self.data = []
        self.i_fname = None
        self.i_file = None
        self.o_fname = None
        self.o_file = None
        
        if inputfile:
            self.i_fname = inputfile
            self.i_file = open(inputfile)
        if outputfile:
            self.o_fname = outputfile
            self.o_file = open(outputfile, "w+")

    def parse(self):
        if self.i_file:
            self.rawhtml = self.i_file.read()
            self.feed(self.rawhtml)

    def close(self):
        if self.i_file:
            self.i_file.close()
        if self.o_file:
            self.o_file.write(self.getData())
            self.o_file.close()

    def getData(self):
        return "\n".join(self.data)
    
    def getLinks(self):
        return self.links
        
    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for name, val in attrs:
                if name == "class":
                    if val == "gaag_course":
                        self.course = True
                    elif val == "gaag_grade":
                        self.grade = True
        elif self.course and tag == "a":
            for name, val in attrs:
                if name == "href":
                    self.cur_link = val

    def handle_data(self, data):
        if self.cur_link:
            self.links.append(self.cur_link)

        if self.course:
            self.data.append(data)
            self.course = False
            if not self.cur_link:
                self.links.append('#') # default link
            self.cur_link = None

        elif self.grade:
            self.data[-1] += " : " + data
            self.grade = False
            
