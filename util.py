

def read_text(file):
    print "reading", file
    stream = open(file, 'r')
    text = stream.read()
    stream.close()
    return text

def write_text(text, file):
    print "writing", file
    stream = open(file, 'w')
    stream.write(text)
    stream.close()

