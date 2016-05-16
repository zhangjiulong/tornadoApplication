#coding=utf-8
__author__ = 'Administrator'
from xml.dom import minidom


def fixedWritexml(self, writer, indent="  ", addindent="", newl="\n"):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))

minidom.Element.writexml = fixedWritexml

def saveXml2File(xmlStr, saveFile):
    doc = minidom.parseString(xmlStr)
    # fixedWritexml(self.getUserRoot().writxml)
    with open(saveFile, 'wb') as xmlFile:
        doc.writexml(xmlFile, addindent='  ',newl='\n',encoding = 'utf-8')
    xmlFile.close()

if __name__ == '__main__':
    pass