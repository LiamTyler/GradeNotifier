from html.parser import HTMLParser

class MoodleGradeParser(HTMLParser):
    def __init__(self, inputfile=None, outputfile=None):
        HTMLParser.__init__(self)
        self.rawhtml = None
        self.course = False
        self.grade = False
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
        
    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for name, val in attrs:
                if name == "class":
                    if val == "gaag_course":
                        self.course = True
                    elif val == "gaag_grade":
                        self.grade = True
    
    def handle_data(self, data):
        if self.course:
            #print("course: ", data)
            self.data.append(data)
            self.course = False
        elif self.grade:
            #print("grade: ", data)
            self.data[-1] += " : " + data
            self.grade = False
            
