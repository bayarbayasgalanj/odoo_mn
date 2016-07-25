openerp.sale_order_schedule = function(instance) {
    openerp.sale_order_schedule.order_route(instance);
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    
    // #################################### sale_order_schedule ##########################################
    instance.sale_order_schedule.order_schedule = instance.web.form.FormWidget.extend(instance.web.form.ReinitializeWidgetMixin, {
        events: {
        },
        init: function() {

            // $("head").append('<script type="text/javascript" src="gps_tracker/static/src/jqwidgets/datepicker/moment.min.js"></script>');
            // $("head").append('<script type="text/javascript" src="gps_tracker/static/src/jqwidgets/datepicker/jquery.daterangepicker.js"></script>');
            
            this._super.apply(this, arguments);
            var self = this;
            this.set({
                schedule: false,
            });
            this.updating = false;
            this.field_manager.on("field_changed:schedule_line", this, this.query_sheets);

            this.res_o2m_drop = new instance.web.DropMisordered();
            this.render_drop = new instance.web.DropMisordered();
            this.description_line = _t("/");
            // Original save function is overwritten in order to wait all running deferreds to be done before actually applying the save.
            this.view.original_save = _.bind(this.view.save, this.view);
            this.view.save = function(prepend_on_create){
                self.prepend_on_create = prepend_on_create;
                return $.when.apply($, self.defs).then(function(){
                    return self.view.original_save(self.prepend_on_create);
                });
            };
            // this.field_manager.on("field_changed:schedule_line", this, function() {
            //     this.set({"schedule": this.field_manager.get_field_value("schedule_line")});
            // });
        },
        query_sheets: function() {
            var self = this;
            var commands = this.field_manager.get_field_value("schedule_line");
            this.res_o2m_drop.add(new instance.web.Model(this.view.model).call("resolve_2many_commands", ["schedule_line", commands, [], 
                        new instance.web.CompoundContext()]))
                    .done(function(res) {
                    self.querying = true;
                    self.set({schedule: res});
                    self.querying = false;
                });
        },
        initialize_field: function() {
            instance.web.form.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:schedule", self, self.initialize_content);
        },
        
        initialize_content: function() {
            var self = this;
            this.destroy_content();
            // var attach_ids = []
            // if (self.get('attach_image')){
            //     attach_ids = self.get('attach_image')[0][2];
            //     return  new instance.web.Model('ir.attachment').call('search', [[['id', 'in', attach_ids],['index_content','=','image'] ]])
            //     .then(function(ids){
            //             self.attach_ids = ids;
            //             self.display_data();
            //     });
            // }

            var schedule;
            self.schedule = self.get('schedule');
            
            self.display_data();
        },
        destroy_content: function() {
            if (this.dfm) {
                this.dfm.destroy();
                this.dfm = undefined;
            }
        },
        display_data: function() {
            var self = this;
            self.$el.html(QWeb.render("sale_order_schedule.order_schedule", {widget: self}));
            // var map;
            // console.log(self.schedule.length);
            
            if (self.schedule.length>2){
                var directs = [];
                var origin = {'lat': self.schedule[0].partner_latitude, 'lng': self.schedule[0].partner_longitude};
                var destination = {'lat': self.schedule[self.schedule.length-1].partner_latitude, 'lng': self.schedule[self.schedule.length-1].partner_longitude};
                var waypoints = [];
                for (var i=1; i<self.schedule.length-1; i++){
                    // console.log(self.schedule[i]);
                    waypoints.push({'location':{'lat': self.schedule[i].partner_latitude, 'lng': self.schedule[i].partner_longitude}, stopover:true})
                }
                // this.waypoints.push({location:new google.maps.LatLng(points[p][0], points[p][1]),stopover:false});
              
                console.log(directs);
                var directionsService = new google.maps.DirectionsService;
                var directionsDisplay = new google.maps.DirectionsRenderer;
                
                var map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 13,
                  center: {lat: 47.894344, lng: 106.881591}
                });

                directionsDisplay.setMap(map);
                
                directionsService.route({
                  origin: origin,
                  destination: destination,
                  waypoints: waypoints,
                  travelMode: google.maps.TravelMode.DRIVING
                }, function(response, status) {
                  if (status === google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(response);
                  } else {
                    window.alert('Directions request failed due to ' + status);
                  }
                });
            }
            
        },
    });
    
    instance.web.form.custom_widgets.add('order_schedule', 'instance.sale_order_schedule.order_schedule');

};
