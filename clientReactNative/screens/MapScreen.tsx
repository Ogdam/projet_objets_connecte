import React, { useState, useCallback, useEffect } from 'react'
import { Button, NativeSyntheticEvent, StyleSheet, TextInput, TextInputSubmitEditingEventData } from 'react-native';
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { GiftedChat, IMessage } from 'react-native-gifted-chat'
import MapView, {Polyline, Marker} from 'react-native-maps';
import { Dimensions } from "react-native";

export default class MapScreen extends React.Component {

  socket = new WebSocket('ws://192.168.1.91:8765');
  state  = { depart: "" , arrive : "", trajet : []};

  componentDidMount(){
    var self = this
    this.socket.onmessage = function(this: WebSocket, ev: MessageEvent){
      self.setState({ trajet: JSON.parse(ev.data) });
    };
  }

  componentWillUnmount(){
    this.socket.close()
  }

  handleSubmit(this: any){
    this.socket.send("Aller de "+this.state.depart+" a "+this.state.arrive)
  }

  render(){
    return (
      <View style={styles.container}>
        <MapView
            style={styles.map}
            initialRegion={{
            latitude: 48.8534,
            longitude: 2.3488,
            latitudeDelta: 0.0922,
            longitudeDelta: 0.0421,
          }}>
          {this.state.trajet.map((marker : any) => {
            <Polyline
              coordinates={[ {'latitude' : Number(marker['from'][0]['lat']), 'longitude' : Number(marker['from'][0]['lng'])},
                             {'latitude' : Number(marker['to'][0]['lat']), 'longitude' : Number(marker['to'][0]['lng'])}
                           ]}
               strokeWidth={1}
               strokeColor="red"
               fillColor="rgba(255,0,0,0.5)"
            />
          })
         }
        </MapView>
        <View>
        // mettre trajet txt
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
    bottom: 500,
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

  }
});
