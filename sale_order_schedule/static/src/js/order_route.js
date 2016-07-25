openerp.sale_order_schedule.order_route = function(instance) {
    
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    
    // #################################### order route ##########################################
    instance.sale_order_schedule.order_route = instance.web.form.FormWidget.extend(instance.web.form.ReinitializeWidgetMixin, {
        events: {
        },
        init: function() {

            // $("head").append('<script type="text/javascript" src="gps_tracker/static/src/jqwidgets/datepicker/moment.min.js"></script>');
            // $("head").append('<script type="text/javascript" src="gps_tracker/static/src/jqwidgets/datepicker/jquery.daterangepicker.js"></script>');
            
            this._super.apply(this, arguments);
            var self = this;
            this.set({
                route: false,
            });
            this.updating = false;
            this.field_manager.on("field_changed:route_line", this, this.query_sheets);

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
            var commands = this.field_manager.get_field_value("route_line");
            this.res_o2m_drop.add(new instance.web.Model(this.view.model).call("resolve_2many_commands", ["route_line", commands, [], 
                        new instance.web.CompoundContext()]))
                    .done(function(res) {
                    self.querying = true;
                    self.set({route: res});
                    self.querying = false;
                });
        },
        initialize_field: function() {
            instance.web.form.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:route", self, self.initialize_content);
        },
        
        initialize_content: function() {
            var self = this;
            this.destroy_content();
            
            var route;
            self.route = self.get('route');
            
            // if (self.route.length>0){
            //     var sss = new instance.web.Model("sale.order.zone.lat").call("search", [[["zone_id", "=", self.route.zone_id[0]], ]])
            //         .then(function(ids) {
            //         var rrr = new instance.web.Model("sale.order.zone.lat").call("read", [ids,[]]).then(function(details){
                        
            //         });           
            //     });
            // }
            
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
            self.$el.html(QWeb.render("sale_order_schedule.order_route", {widget: self}));
            
            var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 14,
              center: {lat: 47.894344, lng: 106.881591},
              // mapTypeId: google.maps.MapTypeId.TERRAIN
            });

            for (var i=0; i<self.route.length; i++){
                var sss = new instance.web.Model("sale.order.zone.lat").call("search", [[["zone_id", "=", self.route[i].zone_id[0]], ]])
                    .then(function(ids) {
                    var rrr = new instance.web.Model("sale.order.zone.lat").call("read", [ids,[]]).then(function(details){
                        var zoneCoors = [];
                        for (j=0; j<details.length; j++){
                            zoneCoors.push({'lat': details[j].latitude, 'lng': details[j].longitude});
                        }
                        
                        if (details.length>0){
                            zoneCoors.push({'lat': details[details.length-1].latitude, 'lng': details[details.length-1].longitude});
                        }
                       var zonePath = new google.maps.Polygon({
                            paths: zoneCoors,
                            strokeColor: '#FF0000',
                            strokeOpacity: 0.8,
                            strokeWeight: 2,
                            fillColor: '#FF0000',
                            fillOpacity: 0.35
                        });
                        zonePath.setMap(map);
                        console.log(zoneCoors);
                        
                    });           
                });
            }
            map.data.setStyle({
              icon: '//example.com/path/to/image.png',
              fillColor: 'green'
            });
            // for (var i=0; i<self.route.length; i++){
            //     // console.log(self.route[i]);
            //     if (self.route[i].is_view){
            //         var rectangle = new google.maps.Rectangle({
            //           strokeColor: self.route[i].color,
            //           strokeOpacity: 0.8,
            //           strokeWeight: 2,
            //           fillColor: self.route[i].color,
            //           fillOpacity: 0.35,
            //           title:'asdf',
            //           map: map,
            //           bounds: {
            //             north: self.route[i].north,// 33.685,
            //             south: self.route[i].south,// 33.671,
            //             east: self.route[i].east,//-116.234,
            //             west: self.route[i].west,//-116.251
            //           }
            //           });
            //         var marker = new google.maps.Marker({
            //           position: new google.maps.LatLng(self.route[i].north,self.route[i].east),
            //           label:  {
            //             text: 'label',
            //             // Add in the custom label here
            //             // fontFamily: 'Roboto, Arial, sans-serif, custom-label-' + label
            //           },
            //           labelContent:'asdf',
            //           map: map
            //         });
                    
            //     }
            // }
            
        },
    });
    
    instance.web.form.custom_widgets.add('order_route', 'instance.sale_order_schedule.order_route');

};
