import rdflib
from rdflib import Graph
from rdflib import URIRef, RDF, RDFS


def executeQuery(query, g):
    return g.query(query)


def getGoal(g):
    """query = 'select ?s	?v  where { ?s rdf:type or:RegleEevenement . ?s or:lancer ?v . ?s or:limiteMin ?lmin . ?s or:limiteMax ?lmax .  FILTER( xsd:integer(?lmin) <= '+str(x)+' && xsd:integer(?lmax) > '+str(x)+' ) . }'"""
    query = 'select ?s where { ?s rdf:type go:Goal}'
    rows = executeQuery(query, g)
    for row in rows:
        print(row.s)
        """print(row.s.rsplit('#')[-1])"""


def askGoal0(g):
    query = 'PREFIX  resour1: <file:///C:/Users/mbeggas/Google%20Drive/json-test/ontologies/instaceonto.rdfs#> \n'
    query = 'select ?p ?o where{ '
    query += ' resour1:maingoal ?p ?o}'

    print(query)
    rows = executeQuery(query, g)
    print(rows)
    for row in rows:
        print(row)


def askGoal1(g, size):
    query = 'ASK { '
    query += ' <file:///C:/Users/mbeggas/Google Drive/json-test/ontologies/instaceonto.rdfss#g1> go:minImageSize ?goalmin .'
    query += ' <file:///C:/Users/mbeggas/Google Drive/json-test/ontologies/instaceonto.rdfs#g1> go:maxImageSize ?goalmax .'
    query += '  FILTER(xsd:decimal(?goalmin) <= ' + str(size) + ' && xsd:decimal(?goalmax) >= ' + str(size) + ') .}'
    rows = executeQuery(query, g)
    print(rows.askAnswer)


def askGoal2(g, imageFormat):
    query = 'ASK where{ '
    query += ' <file:///C:/Users/othma/Desktop/dr/monir/InstancesGoal.rdfs#g1> go:ImageFormat ' + str(
        imageFormat) + ' .'
    query += ' }'

    rows = executeQuery(query, g)
    print(rows.askAnswer)


if __name__ == '__main__':
    g = rdflib.Graph()
    rdffile = 'ontologies/instaceonto.rdfs'
    g.load(rdffile)
    # getGoal(g)

    askGoal0(g)
    #
    # imageFormat = '<file:///C:/Users/othma/Desktop/dr/monir/InstancesGoal.rdfs#jpg>'
    # size = 200
    # askGoal2(g, size)
    # askGoal2(g, imageFormat)
    #
    # """for s,p,o in g:
    #     print s,p,o"""
