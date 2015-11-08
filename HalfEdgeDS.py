import param
import math

# A mesh contains:
# Vertices, HalfEdges (and Edges), and Cells
class Mesh:
  def __init__(self):
    self.verts = {}
    self.cells = {}
    self.halfedges = {}
    self.edges = {}

  def addVertex(self, v):
    self.verts.append(v)

  # For a hexagonal cell
  # TODO: Generalize for n-gon and not just hexagons  
  def addCell(self, v1, v2, v3, v4, v5, v6):

    # Generate a new cell
    cell_counter = len(self.cells)-1
    cell = Cell(cell_counter+1,0,0)    

    # How many half edges do we currently have?
    halfedge_counter = len(self.halfedges)-1

    # Generate the half edges
    he_1 = HalfEdge(halfedge_counter+1,v2,cell)
    he_2 = HalfEdge(halfedge_counter+2,v3,cell)
    he_3 = HalfEdge(halfedge_counter+3,v4,cell)
    he_4 = HalfEdge(halfedge_counter+4,v5,cell)
    he_5 = HalfEdge(halfedge_counter+5,v6,cell)
    he_6 = HalfEdge(halfedge_counter+6,v1,cell)

    # Generate the half edge pairs (outer edges) with no cells
    hep_1 = HalfEdge(halfedge_counter+7,v1,None)
    hep_2 = HalfEdge(halfedge_counter+8,v2,None)
    hep_3 = HalfEdge(halfedge_counter+9,v3,None)
    hep_4 = HalfEdge(halfedge_counter+10,v4,None)
    hep_5 = HalfEdge(halfedge_counter+11,v5,None)
    hep_6 = HalfEdge(halfedge_counter+12,v6,None)    

    # Connect the cell to only one half edge
    # The cell only needs to know halfedge to traverse the cell boundaries
    cell.halfedge = he_1
    self.cells[cell.uid] = cell

    # Add one half edge to one vertex
    v1.halfedge = he_1
    v2.halfedge = he_2
    v3.halfedge = he_3
    v4.halfedge = he_4
    v5.halfedge = he_5
    v6.halfedge = he_6

    # Construct half edge connectivities
    he_1.next = he_2
    he_2.next = he_3
    he_3.next = he_4
    he_4.next = he_5
    he_5.next = he_6
    he_6.next = he_1

    he_1.prev = he_6
    he_2.prev = he_1
    he_3.prev = he_2
    he_4.prev = he_3
    he_5.prev = he_4
    he_6.prev = he_5

    # Construct half edge pair connectivities
    hep_1.next = hep_6
    hep_2.next = hep_1
    hep_3.next = hep_2
    hep_4.next = hep_3
    hep_5.next = hep_4
    hep_6.next = hep_5

    hep_1.prev = hep_2
    hep_2.prev = hep_3
    hep_3.prev = hep_4
    hep_4.prev = hep_5
    hep_5.prev = hep_6
    hep_6.prev = hep_1

    # Construct edges from half edges
    # How many edges do we currently have?
    edge_counter = len(self.edges)-1

    e1 = Edge(edge_counter+1, he_1, hep_1) 
    e2 = Edge(edge_counter+2, he_2, hep_2) 
    e3 = Edge(edge_counter+3, he_3, hep_3) 
    e4 = Edge(edge_counter+4, he_4, hep_4) 
    e5 = Edge(edge_counter+5, he_5, hep_5) 
    e6 = Edge(edge_counter+6, he_6, hep_6) 

    he_1.pair = hep_1  
    he_2.pair = hep_2 
    he_3.pair = hep_3 
    he_4.pair = hep_4 
    he_5.pair = hep_5 
    he_6.pair = hep_6

    hep_1.pair = he_1 
    hep_2.pair = he_2 
    hep_3.pair = he_3 
    hep_4.pair = he_4 
    hep_5.pair = he_5 
    hep_6.pair = he_6 

    he_1.edge = e1  
    he_2.edge = e2  
    he_3.edge = e3  
    he_4.edge = e4  
    he_5.edge = e5  
    he_6.edge = e6  

    hep_1.edge = e1  
    hep_2.edge = e2  
    hep_3.edge = e3  
    hep_4.edge = e4  
    hep_5.edge = e5  
    hep_6.edge = e6

    # Store the constructed edges and halfedges)
    self.halfedges[he_1.uid] = he_1
    self.halfedges[he_2.uid] = he_2
    self.halfedges[he_3.uid] = he_3
    self.halfedges[he_4.uid] = he_4
    self.halfedges[he_5.uid] = he_5
    self.halfedges[he_6.uid] = he_6

    self.halfedges[hep_1.uid] = hep_1
    self.halfedges[hep_2.uid] = hep_2
    self.halfedges[hep_3.uid] = hep_3
    self.halfedges[hep_4.uid] = hep_4
    self.halfedges[hep_5.uid] = hep_5
    self.halfedges[hep_6.uid] = hep_6

    self.edges[e1.uid] = e1
    self.edges[e2.uid] = e2
    self.edges[e3.uid] = e3
    self.edges[e4.uid] = e4
    self.edges[e5.uid] = e5
    self.edges[e6.uid] = e6

    # @Tests
    # Inner halfedges should all contain cell
    # Prev halfedges should be pointing to next halfedges
    for hedge in list(cell.cellHalfEdgeIterator()):
      assert hedge.cell == cell
      previous_hedge = hedge.prev
      assert previous_hedge.next == hedge
      next_hedge = hedge.next
      assert next_hedge.prev == hedge

    # Outer halfedges shoud not be associated with any cells
    for hedge in list(cell.cellHalfEdgeIterator()):
      # print(hedge.pair.uid)
      # wait = input('')
      assert hedge.pair.cell == None   
      previous_hedge = hedge.prev
      assert previous_hedge.next == hedge
      next_hedge = hedge.next
      assert next_hedge.prev == hedge         

    # Halfedges in each edge should contain the right pairs
    for edge in list(cell.cellEdgeIterator()):
      assert edge.first.pair == edge.second
      assert edge.second.pair == edge.first

    return cell

  #################################################
  # This method merges 2 edges by removing the outer
  # halfedges that are not associated with any polygons
  # and pairing the 2 inner edges
  #################################################
  def mergeEdge(self, e1, e2):

    # for x in self.halfedges:
    #   # print(self.halfedges[x].uid)

    # Halfedges of interest
    he1 = e1.first
    he2 = e2.first

    # Halfedges to be discarded
    he1_ = e1.second
    he2_ = e2.second

    # Make sure that the merge is possible first:
    assert he1.cell != None
    assert he1_.cell == None

    assert he2.cell != None
    assert he2_.cell == None

    # Move all connectivity info to e1:
    he1.pair = he2
    he2.pair = he1
    e1.second = he2

    # Edge information
    assert he1.edge == e1
    he2.edge = e1

    # Fix outer connectivities for he1_:
    tail_1 = he1_.prev
    head_2 = he2_.next

    tail_1.next = head_2
    head_2.prev = tail_1

    tail_2 = he2_.prev
    head_1 = he1_.next

    tail_2.next = head_1
    head_1.prev = tail_2

    # Remove unwanted pieces from the mesh
    print('delete 1', he1_.uid)
    print('delete 2', he2_.uid)    

    del self.halfedges[he1_.uid]
    del self.halfedges[he2_.uid]
    del self.edges[e2.uid]

    # @Tests
    # first hedge's pair should be second hedge
    # second hege's pair should be first hedge
    # first hedge's edge.second should be second hedge
    # unwanted edges and halfedges should now be removed 
    assert he1.pair == he2
    assert he2.pair == he1
    assert e1.second == he2
    assert e2.uid not in self.edges 
    assert he1_.uid not in self.halfedges 
    assert he2_.uid not in self.halfedges 
    assert he1.edge == e1
    assert he2.edge == e1

    ###############################################
  # This method performs a T1Swap on 2 vertices
  #################################################

  def performT1Swap(self, edge):
    print('before swap')
    v = edge.first.vertex
    for e in list(v.vertexHalfEdgeIterator()):
      print('3:', e.edge.uid)
    # input('')  
    v = edge.second.vertex
    for e in list(v.vertexHalfEdgeIterator()):
      print('9:', e.edge.uid)     
    # input('')   

    print('Performing T1 Swap')
    v1 = edge.first.vertex
    v2 = edge.second.vertex
    print('first v, second v: ', v1.uid, v2.uid)
    [x1,y1] = [v1.x,v1.y]
    [x2,y2] = [v2.x,v2.y]
    cx = (x1 + x2) / 2;
    cy = (y1 + y2) / 2;
    def x_new(x,y):
      return ( (x - cx) * math.cos(-90) + (y - cy) * math.sin(-90) ) + cx
    def y_new(x,y):
      return (-(x - cx) * math.sin(-90) + (y - cy) * math.cos(-90) ) + cy
    
    v1.x = x_new(x1,y1)
    v1.y = y_new(x1,y1)
    v2.x = x_new(x2,y2)
    v2.y = y_new(x2,y2)
    
    v1.halfedge = edge.second
    v2.halfedge = edge.first

    halfedges = [edge.first, edge.second]
    for e in halfedges:
      ep = e.prev
      en = e.next
      ep.next = en
      en.prev = ep
      ep.vertex = e.vertex

      en_f = en.pair
      en_f.next = e.pair

      epp = e.prev.pair
      e.next = epp
      epp.prev = e

      eppcell = epp.cell
      ecell = e.cell

      ecell.halfedge = e.prev
      e.cell = epp.cell

    print('Swapping Completed.')  

    # Assertions
    v1_vertices = list(v1.vertexVertexIterator())
    v2_vertices = list(v2.vertexVertexIterator())
    

# A vertex with some information stored
class Vertex:
  def __init__(self, uid, x, y):
    self.uid = uid
    self.x = x
    self.y = y
    self.halfedge = None # A halfedge pointing out from this vertex

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  # Gets the normal of this vertex belonging to cell c
  def getNormal(self, c):
    currentCell = False
    while currentCell != c:
      currentCell = self.halfedge.cell

  # Iterates over all half edges of this vertex
  def vertexHalfEdgeIterator(self):
    this_edge = self.halfedge
    hasMoreEdges = True

    while hasMoreEdges:
      yield this_edge
      # print('Edge pairs: ', this_edge.uid, this_edge.pair.uid)
      next_edge = this_edge.pair.next
      
      if (next_edge.uid == self.halfedge.uid):
        hasMoreEdges = False

      this_edge = next_edge

  # Finds the neighbouring vertices
  def vertexVertexIterator(self):
    this_edge = self.halfedge
    hasMoreEdges = True

    while hasMoreEdges:
      yield this_edge.vertex
      # print('Edge pairs: ', this_edge.uid, this_edge.pair.uid)
      next_edge = this_edge.pair.next
      
      if (next_edge.uid == self.halfedge.uid):
        hasMoreEdges = False

      this_edge = next_edge

  def vertexCellIterator(self):
    this_edge = self.halfedge
    # print('iterator uid: ', this_edge.uid)
    # print('iterator cell uid: ', this_edge.cell.uid)
    hasMoreEdges = True

    while hasMoreEdges:
      if this_edge.cell != None:
        yield this_edge.cell

      next_edge = this_edge.pair.next

      if (next_edge.uid == self.halfedge.uid):
        hasMoreEdges = False

      this_edge = next_edge

# A halfedge object containing all important connectivities
class HalfEdge:
  def __init__(self, uid, vertex, cell=None):
    self.uid = uid
    self.vertex = vertex # The vertex this half_edge is pointing to
    self.cell = cell
    self.pair = None
    self.next = None
    self.prev = None
    self.edge = None # store reference to an edge with 2 half edges

# Edge stores 2 half edges
class Edge:
  def __init__(self, uid, first, second):
    self.uid = uid
    self.first = first
    self.second = second
    self.isAPEdge = False
    
  # How do we determine if this a boundary edge?
  # If either one of the halfedges is not associated with a cell, then it is a boundary edge
  def isBoundary(self):
    if self.second.cell == None or self.first.cell == None:
      return True
    return False  

  def setBaz(self, baz):
    self.baz = baz
  def setMyo(self, myo):
    self.myo = myo
  def setShroom(self, shrm):
    self.shroom = shrm
  def setRok(self, rok):
    self.rok = rok

  def getLength(self):
    v1 = self.first.vertex
    v2 = self.second.vertex
    return math.hypot(v2.x - v1.x, v2.y - v1.y) # Builtin distance formula sqrt(xx + yy)

  # Intermediate length in runge-kutta timestep
  def getTmpLength(self):
    v1 = self.first.vertex
    v2 = self.second.vertex
    return math.hypot(v2.x_tmp - v1.x_tmp, v2.y_tmp - v1.y_tmp) # Builtin distance formula sqrt(xx + yy)

class Cell:
  def __init__(self,uid,x,y):
    # defines the centroid of this cell
    self.uid = uid
    self.x = 0
    self.y = 0
    self.halfedge = 0    # Stores one of the half edges bordering it
 
  def setPhi(self, phi):
    self.phi = phi 

  def setX(self,x):
    self.x = x
  
  def setY(self,y):
    self.y = y

  def getX(self):
    return self.x
  
  def getY(self):
    return self.y

  def getArea(self):
    poly = []
    total = 0.0
    for v in list(self.cellVertexIterator()): # Collect vertices:
      poly.append((v.x,v.y))
    N = len(poly)
    for i in range(N): # Shoelace algorithm for polygon area:
        v1 = poly[i]
        v2 = poly[(i+1) % N]
        total += v1[0]*v2[1] - v1[1]*v2[0]
    return abs(total/2)

  def getTmpArea(self):
    poly = []
    total = 0.0
    for v in list(self.cellVertexIterator()): # Collect vertices:
      # print(v.x_tmp)
      poly.append((v.x_tmp,v.y_tmp))
    N = len(poly)
    for i in range(N): # Shoelace algorithm for polygon area:
        v1 = poly[i]
        v2 = poly[(i+1) % N]
        total += v1[0]*v2[1] - v1[1]*v2[0]
    return abs(total/2)

  ######################
  # Iterators
  ######################

  # Iterates over all half edges of this cell
  def cellHalfEdgeIterator(self):
    this_hedge = self.halfedge
    hasMoreEdges = True

    while hasMoreEdges:
      yield this_hedge
      next_hedge = this_hedge.next
      #print('Edge', this_hedge.uid, 'points to Edge', next_hedge.uid)

      if next_hedge.uid == self.halfedge.uid:
        hasMoreEdges = False

      this_hedge = next_hedge    

  # Iterates over all vertices of this cell
  def cellVertexIterator(self):
    this_hedge = self.halfedge
    hasMoreVertices = True

    while hasMoreVertices:
      assert (this_hedge.vertex != None)
      yield this_hedge.vertex
      next_hedge = this_hedge.next

      if next_hedge.vertex.uid == self.halfedge.vertex.uid:
        hasMoreVertices = False

      this_hedge = next_hedge  

  # Iterates over all vertices of this cell + initial vertex once more
  # For plotting
  def cellVertexPlotIterator(self):
    this_hedge = self.halfedge
    hasMoreVertices = True

    while hasMoreVertices:
      assert (this_hedge.vertex != None)
      yield this_hedge.vertex
      next_hedge = this_hedge.next

      if next_hedge.vertex.uid == self.halfedge.vertex.uid:
        yield next_hedge.vertex
        hasMoreVertices = False

      this_hedge = next_hedge  

  # Iterates over all edges of this cell
  def cellEdgeIterator(self):
    this_hedge = self.halfedge
    hasMoreEdges = True

    while hasMoreEdges:
      yield this_hedge.edge
      next_hedge = this_hedge.next
      #print('Edge', this_hedge.uid, 'points to Edge', next_hedge.uid)

      if next_hedge.uid == self.halfedge.uid:
        hasMoreEdges = False

      this_hedge = next_hedge      

  # Iterates over all the neighbours of this cell
  def cellCellIterator(self):    
    this_hedge = self.halfedge
    hasMoreEdges = True

    while hasMoreEdges:
      if this_hedge.pair != None:
        this_hedge.pair.cell

      next_hedge = this_hedge.next
      if next_hedge.uid == self.halfedge.uid:
        hasMoreEdges = False

      this_hedge = next_hedge
