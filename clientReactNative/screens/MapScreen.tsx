import React, { useState, useCallback, useEffect } from 'react'
import { Button, NativeSyntheticEvent, Switch, StyleSheet, TextInput, TextInputSubmitEditingEventData } from 'react-native';
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { GiftedChat, IMessage } from 'react-native-gifted-chat'
import MapView, {Polyline, Marker} from 'react-native-maps';
import { Dimensions } from "react-native";

export default class MapScreen extends React.Component {

  socket = new WebSocket('ws://192.168.1.91:8765');
  state  = { depart: "" , arrive : "", trajet : {'transport' : [], 'car' : []}, choice : true};

  componentDidMount(){
    var self = this
    this.socket.onmessage = function(this: WebSocket, ev: MessageEvent){
      self.setState({ trajet: { 'transport' : JSON.parse(ev.data), "car" : []} });
    };
  }

  componentWillUnmount(){
    this.socket.close()
  }

  handleSubmit(this: any){
    this.socket.send("Aller de "+this.state.depart+" a "+this.state.arrive)
  }

  random_rgba() {
    var o = Math.round, r = Math.random, s = 255;
    return 'rgba(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) + ',' + 1 + ')';
  }

  transport(){
    return ( <View>
      <Text style={styles.text}>Public Transport</Text>
      {this.state.trajet.transport.map((marker : any, indext: Number) => {
        if (marker.type == "walking"){
            <Text style={styles.text} key={"type"+indext} >{marker.type}</Text>
            return marker['path'].map((walk: any, index : Number) => {
              return <Text style={styles.text} key={"walk"+index} > - marcher { walk.name } </Text>
            })

        }
        if (marker['type'] !== "walking"){
          return(
          <View>
            <Text style={styles.text} key={"type"+indext} >{marker.type} ligne {marker.label}</Text>
            <Text style={styles.text} key={"from"+indext} > - de : {marker.from.name}</Text>
            <Text style={styles.text} key={"to"+indext}   > - a : {marker.to.name}</Text>
          </View>)
        }
      })}
      </View>
    )
  }

  render(){
    return (
      <View style={styles.container}>
      <MapView key="map"
          style={styles.map}
          initialRegion={{
          latitude: 48.8534,
          longitude: 2.3488,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}>
        {this.state.choice && this.state.trajet['transport'].map((marker : any, index) => {
          var rgb = this.random_rgba()
          var coord: any = [];
          coord.push({'latitude' : Number(marker.from.lat), 'longitude' : Number(marker.from.lng)})
          if(marker.type == 'walking'){
                marker.coord.forEach((co : any) =>{
                  coord.push({'latitude' : Number(co[1]), 'longitude' : Number(co[0]) } )
                }
              )
          }
          coord.push({'latitude' : Number(marker.to.lat), 'longitude' : Number(marker.to.lng)})
          console.log(coord)
          return <Polyline key={"p1"+index}
            coordinates={coord}
             strokeWidth={3}
             strokeColor= {rgb}
             fillColor="rgba(255,0,0,0.5)"
          />
        })
       }
       {!this.state.choice && this.state.trajet['car'].map((marker : any, index) => {
         var rgb = this.random_rgba()
         return <Polyline key={"p2"+index}
           coordinates={[ {'latitude' : Number(marker.from.lat), 'longitude' : Number(marker.from.lng)},
                          {'latitude' : Number(marker.to.lat), 'longitude' : Number(marker.to.lng)}
                        ]}
            strokeWidth={3}
            strokeColor= {rgb}
            fillColor="rgba(255,0,0,0.5)"
         />
       })
      }
      </MapView>
        <View style={styles.trajet}>
          <Switch
              trackColor={{ false: "#767577", true: "#81b0ff" }}
              thumbColor={this.state.choice ? "#f5dd4b" : "#f4f3f4"}
              ios_backgroundColor="#3e3e3e"
              onValueChange={() => this.setState({choice : !this.state.choice})}
              value={this.state.choice}
            />
          <View>
          {this.state.choice &&
              this.transport()
          }
          {!this.state.choice &&
              <Text style={styles.text}>Car</Text>
          }
          </View>
        </View>
        <View style={styles.message}>
            <TextInput
                style={styles.input}
                multiline={true}
                numberOfLines={4}
                placeholder="départ"
                onChangeText={(text) => this.setState({depart : text})}
                value={this.state.depart}/>
            <TextInput
                style={styles.input}
                multiline={true}
                numberOfLines={4}
                placeholder="arrivé"
                onChangeText={(text) => this.setState({arrive : text})}
                value={this.state.arrive}/>
        </View>
        <View style={styles.btn}>
          <Button
            onPress={this.handleSubmit.bind(this)}
            title="GO"
            color="#841584"
          />
        </View>
      </View>
    );
  }

}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'flex-end',
    alignItems: 'center',
    flex: 1,
  },
  map: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: Dimensions.get('window').height-350,
  },
  trajet : {
    position : 'absolute',
    top : Dimensions.get('window').height-565,
    width : Dimensions.get('window').width,
    height : Dimensions.get('window').width-35,
    backgroundColor : "white"
  },
  message : {
    position: 'absolute',
    bottom:0,
    left: 0,
    height:80,
    flex: 1
  },
  input : {
    height : 40,
    backgroundColor: 'white',
    fontWeight : 'bold',
    borderBottomLeftRadius: 10,
    borderBottomRightRadius: 10,
    borderTopLeftRadius: 10,
    borderTopRightRadius: 10,
    width : Dimensions.get('window').width-60,
    borderStyle : 'solid',
    borderColor : 'black',
    borderWidth : 1
  },
  btn : {
    position: 'absolute',
    bottom:
    20,
    left : Dimensions.get('window').width-40
  },
  text: {
    color : 'black',
    backgroundColor : "white",
    fontSize: 10,
    fontWeight: "bold",
  }
});
