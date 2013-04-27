(function(){

    var Note = Backbone.Model.extend({
        defaults: {
            body: "",
            focussed: false,
            is_feedback: false,
            is_checkin: false
        }
    });

    var NoteCollection = Backbone.Collection.extend({
        model: Note
    });

    var Notes = new NoteCollection();
    
    var FocussedNoteController = Backbone.Marionette.Controller.extend({
        initialize: function() {
            this.focussed = null;
        },
        focusOn: function(note) {
            if(this.focussed) {
                this.focussed.set({focussed: false});
            }
            this.focussed = note;
            this.focussed.set({focussed: true});
            this.trigger("note:focussed");
        }
    });

    var Focussed = new FocussedNoteController();

    var NoteView = Backbone.Marionette.ItemView.extend({
        template: "#note-tmpl",
        tagName: "li",
        className: "note",
        initialize: function() {
            this.model.bind('change', this.render, this);
        },
        events: {
            'keydown .body': 'handleKeydown',
            'keyup .body': 'handleKeyup',
            'click .is-feedback': 'toggleIsFeedback',
            'click .is-checkin': 'toggleIsCheckin'
        },
        handleKeydown: function(e){
            if(e.which == 13) {
                var n = new Note();
                Focussed.focusOn(n);
                Notes.push(n);
                e.preventDefault();
            } 
        },
        handleKeyup: function(e) {
            var val = this.$('.body').val();
            this.model.set({body: val});
        },
        toggleIsFeedback: function(e){
            var checked = $(e.target).is(":checked");
            this.model.set({is_feedback: checked});
        },
        toggleIsCheckin: function(e){
            var checked = $(e.target).is(":checked");
            this.model.set({is_checkin: checked});
        },
        onRender: function() {
            console.log("here");
            if(this.model.get('focussed')) {
                this.$el.addClass("focussed");

                var self = this;
                setTimeout(function(){
                    self.$(".body").focus();
                }, 10);
            } else {
                this.$el.removeClass("focussed");
            }
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
        var notes_field = $("#notes-field");
        $("#entry-form").submit(function(){
            notes_field.val(JSON.stringify(Notes.toJSON()));
            return true;
        });

        var notes_view = new NotesView({collection: Notes});

        notes_view.listenTo(Focussed, "note:focussed", function(stuff){
            this.render();
        });

        var n = new Note();
        Focussed.focusOn(n);
        Notes.push(n);

        App.notes.show(notes_view);
    });

    App.start();

})();
