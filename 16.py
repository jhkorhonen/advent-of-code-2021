
from math import prod

# oh god why is this not enum
type_literal = 4
type_sum = 0
type_product = 1
type_min = 2
type_max = 3
type_gt = 5
type_lt = 6
type_eq = 7

def parse(expr, n = None):
    new_nodes = []
    while len(expr) > 0 and (n is None or len(new_nodes) < n):
        next_node, expr = parse_packet(expr)
        new_nodes.append(next_node)
    return new_nodes, expr

def parse_packet(expr):
    version, packet_type, expr = int(expr[0:3],2), int(expr[3:6],2), expr[6:]
    if packet_type == type_literal:
        next_node, expr = parse_literal(version,expr)
    else:
        next_node, expr = parse_operator(version,packet_type,expr)
    return next_node, expr


def parse_literal(version, expr):
    number_bits = ""
    while True:
        next_bits, expr = expr[0:5], expr[5:]
        if next_bits[0] == "1":
            number_bits += next_bits[1:] 
        else:
            number_bits += next_bits[1:] 
            break
    return tree_node.literal(version, int(number_bits,2)), expr

def parse_operator(version,operator,expr):
    mode, expr = expr[0], expr[1:]
    if mode == "0":
        bits_to_read,expr = int(expr[:15],2), expr[15:]
        children, _ = parse(expr[:bits_to_read])
        expr = expr[bits_to_read:]
    if mode == "1":
        num_children,expr = int(expr[:11],2), expr[11:]
        children, expr = parse(expr, num_children)
    return tree_node.operator(version,operator,children), expr
    

class tree_node:
    def __init__(self,version,node_type):
        self.version = version
        self.node_type = node_type
        self.children = []
        self.value = -1
    
    def __str__(self):
        if self.node_type == type_literal:
            return "Literal v{}:  {}".format(self.version, self.value)
        else:
            return "Operator v{}: {} ({} children)".format(self.version, self.node_type, len(self.children))
            
    def print_node(self,prefix = ""):
        if self.node_type == type_literal:
            print(prefix + str(self))
        else:
            print(prefix + str(self))
            for c in self.children:
                c.print_node(prefix + "-")
    
    def total_version(self):
        return self.version + sum(c.total_version() for c in self.children)
    
    def evaluation(self):
        if self.node_type == type_literal:
            return self.value
        elif self.node_type == type_sum:
            return sum(c.evaluation() for c in self.children)   
        elif self.node_type == type_product:
            return prod(c.evaluation() for c in self.children)
        elif self.node_type == type_min:
            return min(c.evaluation() for c in self.children)
        elif self.node_type == type_max:
            return max(c.evaluation() for c in self.children)
        elif self.node_type == type_gt:
            return 1 if self.children[0].evaluation() > self.children[1].evaluation() else 0
        elif self.node_type == type_lt:
            return 1 if self.children[0].evaluation() < self.children[1].evaluation() else 0
        elif self.node_type == type_eq:
            return 1 if self.children[0].evaluation() == self.children[1].evaluation() else 0
    
    @classmethod
    def literal(cls, version, value):
        new_node = tree_node(version,type_literal)
        new_node.value = value
        return new_node
        
    @classmethod
    def operator(cls, version, operator, children):
        new_node = tree_node(version,operator)
        new_node.children = children
        return new_node

data = "020D78804D397973DB5B934D9280CC9F43080286957D9F60923592619D3230047C0109763976295356007365B37539ADE687F333EA8469200B666F5DC84E80232FC2C91B8490041332EB4006C4759775933530052C0119FAA7CB6ED57B9BBFBDC153004B0024299B490E537AFE3DA069EC507800370980F96F924A4F1E0495F691259198031C95AEF587B85B254F49C27AA2640082490F4B0F9802B2CFDA0094D5FB5D626E32B16D300565398DC6AFF600A080371BA12C1900042A37C398490F67BDDB131802928F5A009080351DA1FC441006A3C46C82020084FC1BE07CEA298029A008CCF08E5ED4689FD73BAA4510C009981C20056E2E4FAACA36000A10600D45A8750CC8010989716A299002171E634439200B47001009C749C7591BD7D0431002A4A73029866200F1277D7D8570043123A976AD72FFBD9CC80501A00AE677F5A43D8DB54D5FDECB7C8DEB0C77F8683005FC0109FCE7C89252E72693370545007A29C5B832E017CFF3E6B262126E7298FA1CC4A072E0054F5FBECC06671FE7D2C802359B56A0040245924585400F40313580B9B10031C00A500354009100300081D50028C00C1002C005BA300204008200FB50033F70028001FE60053A7E93957E1D09940209B7195A56BCC75AE7F18D46E273882402CCD006A600084C1D8ED0E8401D8A90BE12CCF2F4C4ADA602013BC401B8C11360880021B1361E4511007609C7B8CA8002DC32200F3AC01698EE2FF8A2C95B42F2DBAEB48A401BC5802737F8460C537F8460CF3D953100625C5A7D766E9CB7A39D8820082F29A9C9C244D6529C589F8C693EA5CD0218043382126492AD732924022CE006AE200DC248471D00010986D17A3547F200CA340149EDC4F67B71399BAEF2A64024B78028200FC778311CC40188AF0DA194CF743CC014E4D5A5AFBB4A4F30C9AC435004E662BB3EF0"
bits = "".join([format(int(s, 16),"04b") for s in data])

syntax_tree, leftover_expr = parse(bits,1)
syntax_tree = syntax_tree[0]
print(syntax_tree.total_version(),leftover_expr, len(leftover_expr))
print(syntax_tree.evaluation())


