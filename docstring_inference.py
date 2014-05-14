from astroid import MANAGER, UseInferenceDefault, inference_tip, YES, InferenceError, nodes
from astroid.builder import AstroidBuilder

import xml.etree.ElementTree as etree
from docutils.core import publish_doctree

def register(linter):
    pass

def parse_node(node, context, text):
    scope, items = node.scope().scope_lookup(node.scope(), text)
    return items[0].instanciate_class()

def infer_from_docstring(node, context=None):
    for infer in node.func.infer(context.clone()):
        docstring = infer.doc
        if docstring is None:
            break
        
    
        doctree = etree.fromstring(publish_doctree(docstring).asdom().toxml())
        field_lists = doctree.findall(".//field_list")
        fields = [f for field_list in field_lists
                  for f in field_list.findall('field')]

        if fields:
            for field in fields:
                field_name = field.findall("field_name")[0].text
                field_body = field.findall("field_body")[0].findall("paragraph")[0].text
            
                if field_name.startswith("rtype"):
                    ret_node = parse_node(node, context, field_body)
                    return iter([ret_node])
    # found nothing
    raise UseInferenceDefault()

def wrap_exception(node, context=None):
    node._explicit_inference = infer_from_docstring
    return node
        
MANAGER.register_transform(nodes.CallFunc, wrap_exception)

