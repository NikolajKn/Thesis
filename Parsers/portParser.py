# pip3 install requests
# https://github.com/RDFLib/rdflib
import requests
import json
import rdflib
from rdflib.namespace import XSD, RDFS
from datetime import datetime
import csv





class RDF:
    def __init__(self):
        self.g = rdflib.Graph()
        self.SM = rdflib.Namespace('http://www.semanticweb.org/nikolaj/ontologies/2021/3/untitled-ontology-10/')
        self.DBO = rdflib.Namespace('https://dbpedia.org/ontology/')
        self.g.bind("dbo", self.DBO)
        self.g.bind("xsd", XSD)
        self.g.bind("sm", self.SM)

        self.fields = []
        self.data = []
        
        i = 0
        with open("ports.csv") as file:
            csvreader = csv.reader(file)
            self.fields = next(csvreader)
            for row in csvreader:
                self.data.append(row)
                self.createPort(row)
                i += 1
##                if i == 5:
##                    break
            print("Total no. of rows: %d"%(csvreader.line_num))
            

    def createPort(self, data):
        keys = self.fields
        if "-" in data[1]:
            x1 = int(data[1].split("-")[0])
            x2 = int(data[1].split("-")[1])
            for i in range(x1,x2):
                portId = str(i) + data[2]
                self.setPort(portId, str(i))
                self.setProtocol(portId, data)
                self.setType(portId, i, data)
                self.setUnauthorized(portId, data)
        elif data[1] == "":
            return
        else:
            portId = data[1] + data[2]
            self.setPort(portId, data)
            self.setProtocol(portId,  data)
            self.setType(portId, int(data[1]), data)
            self.setUnauthorized(portId, data)


    def setPort(self, id, data):
        self.create_data_property(self.SM + 'Port/' + id, self.SM.hasNumber, data[1], XSD.string)

       
    def setProtocol(self, id, data):
        if data[3] == "Unassigned":
            if data[2] == "tcp":
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["AssignedTCP"])
            elif data[2] == "upd":
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["AssignedUDP"])
            else:
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["DifferentPort"])
        else:
            if data[2] == "tcp":
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["UnassignedTCP"])
            elif data[2] == "upd":
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["UnassignedUDP"])
            else:
                self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["DifferentPort"])


        
    def setType(self, id, port, data):
        if port <= 1023:
            self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["Registered"])
        elif port >= 1024 and port <= 49151:
            self.create_object_property(self.SM + 'Port/' + id, RDFS.Class, self.SM["WellKnown"])
        else:
            self.create_object_property(self.SM + 'Port/' + id,  RDFS.Class, self.SM["Dynamic"])


    def setUnauthorized(self, id, data):
        if data[10] == "":
            self.create_data_property(self.SM + 'Port/' + id, self.SM.unauthorizedUse, "false", XSD.boolean)
        else:
            self.create_data_property(self.SM + 'Port/' + id, self.SM.unauthorizedUse, "true", XSD.boolean)


    def create_object_property(self, uri, property, uri2):
        self.g.add((
            rdflib.URIRef(uri),
            property,
            rdflib.URIRef(uri2),
        ))


    def create_data_property(self, uri, property, data, datatype):
        self.g.add((
            rdflib.URIRef(uri),
            property,
            rdflib.Literal(data, datatype=datatype)
        ))


    def save_graph(self):
        self.g.serialize(format="turtle", destination='ports.rdf')


rdf = RDF()
rdf.save_graph()
