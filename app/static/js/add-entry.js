(function(){

    var Note = Backbone.Model.extend({
        defaults: {
            body: ""
        }
    });

    var NoteCollection = Backbone.Collection.extend({
        model: Note
    });

    var Notes = new NoteCollection();

    var NoteView = Backbone.Marionette.ItemView.extend({
        template: "#note-tmpl",
        tagName: "li",
        className: "note",
        events: {
            'keydown textarea.body': 'handleKeydown'
        },
        handleKeydown: function(e){
            if(e.which == 13) {
                Notes.push(new Note());
                e.preventDefault();
            }
        },
        onRender: function() {
            console.log(this.$el.find("textarea.body"));
            this.$el.find("textarea.body").focus();
        }
    });

    var NotesView = Backbone.Marionette.CollectionView.extend({
        itemView: NoteView,
        tagName: "ul"
    });

    var App = new Backbone.Marionette.Application();    
    
    App.addRegions({
        notes: "#notes"
    });
    
    App.addInitializer(function(){
        Notes.push(new Note());
        var notes_view = new NotesView({collection: Notes});
        App.notes.show(notes_view);
    });

    App.start();
})();
