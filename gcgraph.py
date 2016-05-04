# GCGRAPH
# Maxflow

class Vertex:
	def __init__(self):
		self.next = None # Initialized and used in maxflow() only
		self.parent = 0
		self.first = 0
		self.ts = 0
		self.dist = 0
		self.weight = 0.0
		self.t = None

class Edge:
	def __init__(self):
		self.dst = 0
		self.next = 0
		self.weight = 0.0

class GCGraph:
	def __init__(self, vertex_count, edge_count):
		self.vertexs = []
		self.edges = []
		self.flow = 0
		self .vertex_count = vertex_count
		self.edge_count = edge_count

	def add_vertex(self):
		v = Vertex()
		self.vertexs.append(v)

	def add_edges(self, i, j, w, revw):

		if len(self.edges == 0):
			self.edges = [0, 0]

		fromI = Edge()
		fromI.dst = j
		fromI.next = self.vertexs[i].first
		fromI.weight = w
		vertexs[i].first = len(self.edges)
		self.edges.append(fromI)

		toI = Edge()
		toI.dst = i
		toI.next = self.vertexs[j].first
		toI.weight = revw
		self.vertexs[j].first = len(self.edges)
		self.edges.append(toI)

	def add_term_weights(self, i, source_weight, sink_weight):
		dw = self.vertexs[i].weight
		if dw > 0:
			source_weight += dw
		else:
			sink_weight -= dw
		self.flow += min(source_weight, sink_weight)
		self.vertexs[i].weight = source_weight - sink_weight

	def max_flow(self):
		TERMINAL = -1, ORPHAN = -2
		stub = Vertex()
		nilNode = stub
		first = nilNode
		last = nilNode
		stub.next = nilNode
		curr_ts = 0
		
		orphans = []

		# initialize the active queue and the graph vertices
		for i in range(len(self.vertexs)):
			v = self.vertexs[i]
			v.ts = 0
			if v.weight != 0:
				last = last.next = v
				v.dist = 1
				v.parent = TERMINAL
				v.t = v.weight < 0
			else:
				v.parent = 0
		first = first.next
		last.next = nilNode
		nilNode.next = 0

		while True:
			e0 = -1, ei = 1, ej = 0

			while first != nilNode:
				v = first
				if v.parent:
					vt = v.t
					ei = v.first
					while ei != 0:
						if self.edges[ei^vt].weight == 0:
							continue
						u = self.vertexs[self.edges[ei].dst]
						if not u.parent:
							u.t = vt
							u.parent = ei ^ 1
							u.ts = v.ts
							u.dist = v.dist + 1
							if not u.next:
								u.next = nilNode
								last = last.next = u
							continue
						if u.t != vt:
							e0 = ei ^ vt
							break
						if u.dist > v.dist + 1 and u.ts <= v.ts:
							u.parent = ei ^ 1
							u.ts = v.ts
							u.dist = v.dist + 1
						ei = self.edges[ei].next
					if e0 > 0:
						break
				first = first.next
				v.next = 0
			if e0 <= 0:
				break

			minWeight = self.edges[e0].weight
			for k in range(1, -1, -1):
				v = self.vertexs[self.edges[e0^k].dst]
				while True:
					ei = v.parent
					if ei < 0:
						break
					weight = self.edges[ei^k].weight
					minWeight = min(minWeight, weight)
					v = self.edges[ei].dst
				weight = abs(v.weight)
				minWeight = min(minWeight, weight)
			self.edges[e0].weight -= minWeight
			self.edges[e0^1].weight += minWeight
			self.flow += minWeight

			for k in range(1, -1, -1):
				v = self.vertexs[self.edges[e0^k]].dst
				while True:
					ei = v.parent
					if ei < 0:
						break
					self.edges[ei^(k^1)].weight += minWeight
					self.edges[ei^k].weight -= minWeight
					if self.edges[ei^k].weight == 0:
						orphans.append(v)
						v.parent = ORPHAN
					v = self.vertexs[self.edges[ei]].dst
			curr_ts += 1
			while len(orphans) != 0:
				v2 = orphans[-1]
				orphans.pop()
				minDist = float('inf')
				e0 = 0
				vt = v2.t
				ei = v2.first

				while ei != 0:
					if self.edges[ei^(vt^1)].weight == 0:
						continue
					u = self.vertexs[edges[ei].dst]
					if u.t != vt or u.parent == 0:
						continue

					d = 0
					while True:
						if u.ts == curr_ts:
							d += u.dist
							break
						ej = u.parent
						d += 1
						if ej < 0:
							if ej == ORPHAN:
								d = float('inf') - 1
							else:
								u.ts = curr_ts
								u.dist = 1
							break
						u = self.vertexs[self.edges[ej].dst]

					d += 1
					if d < float("inf"):
						if d < minDist:
							minDist = d
							e0 = ei
						u = self.vertexs[self.edges[ei].dst]
						while u != curr_ts:
							u.ts = curr_ts
							d -= 1
							u.dist = d
							u = self.vertexs[self.edges[u.parent]].dst

					ei = self.edges[ei].next

				v2.parent = e0
				if v2.parent > 0:
					v2.ts = curr_ts
					v2.dist = minDist
					continue

				v2.ts = 0
				ei = v2.first
				while ei != 0:
					u = self.vertexs[self.edges[ei]].dst
					ej = u.parent
					if u.t != vt or (not ej):
						continue
					if self.edges[ei^(vt^1)].weight and (not u.next):
						u.next = nilNode
						last = last.next = u
					if ej > 0 and self.vertexs[self.edges[ej]].dst == v2:
						orphans.append(u)
						u.parent = ORPHAN
					ei = self.edges[ei].next
		return flow

	def insource_segment(i):
		return self.vertexs[i].t == 0
