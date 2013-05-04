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
        },
        url: "/api/notes"
    });

    var Person = Backbone.Model.extend({
    });

    var Feedback = Backbone.Model.extend({
        url: "/api/feedback"
    });

    var PersonCollection = Backbone.Collection.extend({
        model: Person
    });

    var FeedbackCollection = Backbone.Collection.extend({
        model: Feedback
    });

    var People = new PersonCollection();
    
    var NoteCollection = Backbone.Collection.extend({
        model: Note
    });

    var Notes = new NoteCollection();
    var PinnedNotes = new NoteCollection();
    var FeedbackToGive = new FeedbackCollection();

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
    
    var PinnedNoteView = Backbone.Marionette.ItemView.extend({
        template: "#pinned-note-tmpl",
        tagName: "li",
        className: "pinned-note",
        events: {
            "click .unpin-link": 'unpinNote'
        },
        unpinNote: function(e) {
            this.model.set({is_pinned: false});
            this.model.save();
            
            this.$el.hide();

            e.preventDefault();
        }
    });

    var FeedbackView = Backbone.Marionette.ItemView.extend({
        template: "#feedback-tmpl",
        tagName: "li",
        className: "feedback",
        events: {
            "click .communicated-link": 'communicatedFeedback'
        },
        communicatedFeedback: function(e) {
            this.model.set({has_communicated: true});
            this.model.save();
            
            this.$el.hide();

            e.preventDefault();
        }
    });

    var PinnedNotesView = Backbone.Marionette.CollectionView.extend({
        itemView: PinnedNoteView
    });

    var FeedbackCollectionView = Backbone.Marionette.CollectionView.extend({
        itemView: FeedbackView
    });

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
        notes: "#notes",
        pinned_notes: "#pinned-notes",
        feedback: "#feedback"
    });
    
    App.addInitializer(function(){
        People.reset(JSON.parse(managed_by_str));
        PinnedNotes.reset(JSON.parse(pinned_str));
        FeedbackToGive.reset(JSON.parse(feedback_str));

        var notes_field = $("#notes-field");
        $("#entry-form").submit(function(){
            notes_field.val(JSON.stringify(Notes.toJSON()));
            return true;
        });

        var notes_view = new NotesView({collection: Notes});

        var n = new Note();
        Focussed.focusOn(n);
        Notes.push(n);

        var pinned_notes_view = new PinnedNotesView({
            collection: PinnedNotes
        });

        var feedback_view = new FeedbackCollectionView({
            collection: FeedbackToGive
        });

        App.notes.show(notes_view);
        App.pinned_notes.show(pinned_notes_view);
        App.feedback.show(feedback_view);
    });

    App.start();

})();
