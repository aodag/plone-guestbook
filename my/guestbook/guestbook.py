from datetime import datetime

from five import grok
from persistent.list import PersistentList
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from my.guestbook import MessageFactory as _


# Interface class; used to define content-type schema.

class IGuestbook(form.Schema, IImageScaleTraversable):
    """
    example dexterity
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/guestbook.xml to define the content type.

    form.model("models/guestbook.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Guestbook(Container):
    grok.implements(IGuestbook)

    # Add your class methods and properties here
    def __init__(self, *args, **kwargs):
        super(Guestbook, self).__init__(*args, **kwargs)
        self.comments = PersistentList()

    def add_comment(self, name, comment):
        self.comments.append(dict(name=name.decode('utf-8'),
                                  comment=comment.decode('utf-8'),
                                  created_at=datetime.now()))

# View class
# The view will automatically use a similarly named template in
# guestbook_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IGuestbook)
    grok.require('zope2.View')

    grok.name('view')

    # Add view methods here

class Post(grok.View):
    grok.context(IGuestbook)
    grok.require('zope2.View')

    def update(self, name, comment):
        self.context.add_comment(name, comment)

    def render(self):
        return self.redirect(self.url(self.context))
