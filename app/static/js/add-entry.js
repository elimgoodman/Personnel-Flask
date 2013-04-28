(function(){

    var People;
    var Note = Backbone.Model.extend({
        defaults: {
            body: "",
            focussed: false,
            type: "NOTE",
            meta: {}
        },
        initialize: function() {
            //meta defaults
            this.updateMeta('feedback-for', People.at(0).get('id'));
        },
        updateMeta: function(key, val) {
            var meta = this.get('meta');
            meta[key] = val;
            this.set({meta: meta});
        }
    });

    var Person = Backbone.Model.extend({
    });

    var PersonCollection = Backbone.Collection.extend({
        model: Person,
        url: "/api/people/managed_by_current_user",
        parse: function(data) {
            return data.results;
        }
    });
    
    var People = new PersonCollection();
    
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
            'click .note-type': 'changeType',
            'change .meta': 'changeMeta'
        },
        changeMeta: function(e) {
            var target = $(e.target);
            var key = target.data('meta');
            this.model.updateMeta(key, target.val());
            console.log(this.model.toJSON());
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
            this.model.set({body: val}, {silent:true});
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
            if(this.model.get('focussed')) {
                this.$el.addClass("focussed");

                var self = this;
                setTimeout(function(){
                    self.$(".body").focus();
                }, 10);
            } else {
                this.$el.removeClass("focussed");
            }
        },
        templateHelpers: {
            isCheckin: function() {
                return this.type == "CHECKIN";
            },
            isFeedback: function() {
                return this.type == "FEEDBACK";
            },
            isNote: function() {
                return this.type == "NOTE";
            },
            allPeople: function() {
                return People;
            },
            getMeta: function(key) {
                return this.meta[key];
            }
        },
        changeType: function(e) {
            var type = $(e.target);
            this.model.set({type: type.val()});
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
        People.reset(JSON.parse(managed_by_str));

        var notes_field = $("#notes-field");
        $("#entry-form").submit(function(){
            notes_field.val(JSON.stringify(Notes.toJSON()));
            return true;
        });

        var notes_view = new NotesView({collection: Notes});

        var n = new Note();
        Focussed.focusOn(n);
        Notes.push(n);

        App.notes.show(notes_view);
    });

    App.start();

})();
