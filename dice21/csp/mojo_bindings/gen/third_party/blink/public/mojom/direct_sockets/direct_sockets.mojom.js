// third_party/blink/public/mojom/direct_sockets/direct_sockets.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/direct_sockets/direct_sockets.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('blink.mojom');
  var ip_endpoint$ =
      mojo.internal.exposeNamespace('network.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'services/network/public/mojom/ip_endpoint.mojom', '../../../../../services/network/public/mojom/ip_endpoint.mojom.js');
  }
  var mutable_network_traffic_annotation_tag$ =
      mojo.internal.exposeNamespace('network.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'services/network/public/mojom/mutable_network_traffic_annotation_tag.mojom', '../../../../../services/network/public/mojom/mutable_network_traffic_annotation_tag.mojom.js');
  }
  var tcp_socket$ =
      mojo.internal.exposeNamespace('network.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'services/network/public/mojom/tcp_socket.mojom', '../../../../../services/network/public/mojom/tcp_socket.mojom.js');
  }
  var udp_socket$ =
      mojo.internal.exposeNamespace('network.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'services/network/public/mojom/udp_socket.mojom', '../../../../../services/network/public/mojom/udp_socket.mojom.js');
  }



  function DirectSocketOptions(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DirectSocketOptions.prototype.initDefaults_ = function() {
    this.localHostname = null;
    this.localPort = 0;
    this.remotePort = 0;
    this.sendBufferSize = 0;
    this.remoteHostname = null;
    this.receiveBufferSize = 0;
    this.noDelay = false;
  };
  DirectSocketOptions.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DirectSocketOptions.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 40}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketOptions.localHostname
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 0, true)
    if (err !== validator.validationError.NONE)
        return err;



    // validate DirectSocketOptions.remoteHostname
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 16, true)
    if (err !== validator.validationError.NONE)
        return err;





    return validator.validationError.NONE;
  };

  DirectSocketOptions.encodedSize = codec.kStructHeaderSize + 32;

  DirectSocketOptions.decode = function(decoder) {
    var packed;
    var val = new DirectSocketOptions();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.localHostname =
        decoder.decodeStruct(codec.NullableString);
    val.localPort =
        decoder.decodeStruct(codec.Uint16);
    val.remotePort =
        decoder.decodeStruct(codec.Uint16);
    val.sendBufferSize =
        decoder.decodeStruct(codec.Int32);
    val.remoteHostname =
        decoder.decodeStruct(codec.NullableString);
    val.receiveBufferSize =
        decoder.decodeStruct(codec.Int32);
    packed = decoder.readUint8();
    val.noDelay = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  DirectSocketOptions.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DirectSocketOptions.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.NullableString, val.localHostname);
    encoder.encodeStruct(codec.Uint16, val.localPort);
    encoder.encodeStruct(codec.Uint16, val.remotePort);
    encoder.encodeStruct(codec.Int32, val.sendBufferSize);
    encoder.encodeStruct(codec.NullableString, val.remoteHostname);
    encoder.encodeStruct(codec.Int32, val.receiveBufferSize);
    packed = 0;
    packed |= (val.noDelay & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function DirectSocketsService_OpenTcpSocket_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DirectSocketsService_OpenTcpSocket_Params.prototype.initDefaults_ = function() {
    this.options = null;
    this.trafficAnnotation = null;
    this.receiver = new bindings.InterfaceRequest();
    this.observer = new tcp_socket$.SocketObserverPtr();
  };
  DirectSocketsService_OpenTcpSocket_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DirectSocketsService_OpenTcpSocket_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 40}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_Params.options
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, DirectSocketOptions, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_Params.trafficAnnotation
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 8, mutable_network_traffic_annotation_tag$.MutableNetworkTrafficAnnotationTag, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_Params.receiver
    err = messageValidator.validateInterfaceRequest(offset + codec.kStructHeaderSize + 16, false)
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_Params.observer
    err = messageValidator.validateInterface(offset + codec.kStructHeaderSize + 20, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  DirectSocketsService_OpenTcpSocket_Params.encodedSize = codec.kStructHeaderSize + 32;

  DirectSocketsService_OpenTcpSocket_Params.decode = function(decoder) {
    var packed;
    var val = new DirectSocketsService_OpenTcpSocket_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.options =
        decoder.decodeStructPointer(DirectSocketOptions);
    val.trafficAnnotation =
        decoder.decodeStructPointer(mutable_network_traffic_annotation_tag$.MutableNetworkTrafficAnnotationTag);
    val.receiver =
        decoder.decodeStruct(codec.InterfaceRequest);
    val.observer =
        decoder.decodeStruct(new codec.NullableInterface(tcp_socket$.SocketObserverPtr));
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  DirectSocketsService_OpenTcpSocket_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DirectSocketsService_OpenTcpSocket_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(DirectSocketOptions, val.options);
    encoder.encodeStructPointer(mutable_network_traffic_annotation_tag$.MutableNetworkTrafficAnnotationTag, val.trafficAnnotation);
    encoder.encodeStruct(codec.InterfaceRequest, val.receiver);
    encoder.encodeStruct(new codec.NullableInterface(tcp_socket$.SocketObserverPtr), val.observer);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function DirectSocketsService_OpenTcpSocket_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DirectSocketsService_OpenTcpSocket_ResponseParams.prototype.initDefaults_ = function() {
    this.result = 0;
    this.receiveStream = null;
    this.localAddr = null;
    this.peerAddr = null;
    this.sendStream = null;
  };
  DirectSocketsService_OpenTcpSocket_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DirectSocketsService_OpenTcpSocket_ResponseParams.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 40}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;



    // validate DirectSocketsService_OpenTcpSocket_ResponseParams.localAddr
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 8, ip_endpoint$.IPEndPoint, true);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_ResponseParams.peerAddr
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 16, ip_endpoint$.IPEndPoint, true);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_ResponseParams.receiveStream
    err = messageValidator.validateHandle(offset + codec.kStructHeaderSize + 4, true)
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenTcpSocket_ResponseParams.sendStream
    err = messageValidator.validateHandle(offset + codec.kStructHeaderSize + 24, true)
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  DirectSocketsService_OpenTcpSocket_ResponseParams.encodedSize = codec.kStructHeaderSize + 32;

  DirectSocketsService_OpenTcpSocket_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new DirectSocketsService_OpenTcpSocket_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.result =
        decoder.decodeStruct(codec.Int32);
    val.receiveStream =
        decoder.decodeStruct(codec.NullableHandle);
    val.localAddr =
        decoder.decodeStructPointer(ip_endpoint$.IPEndPoint);
    val.peerAddr =
        decoder.decodeStructPointer(ip_endpoint$.IPEndPoint);
    val.sendStream =
        decoder.decodeStruct(codec.NullableHandle);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  DirectSocketsService_OpenTcpSocket_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DirectSocketsService_OpenTcpSocket_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.result);
    encoder.encodeStruct(codec.NullableHandle, val.receiveStream);
    encoder.encodeStructPointer(ip_endpoint$.IPEndPoint, val.localAddr);
    encoder.encodeStructPointer(ip_endpoint$.IPEndPoint, val.peerAddr);
    encoder.encodeStruct(codec.NullableHandle, val.sendStream);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function DirectSocketsService_OpenUdpSocket_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DirectSocketsService_OpenUdpSocket_Params.prototype.initDefaults_ = function() {
    this.options = null;
    this.receiver = new bindings.InterfaceRequest();
    this.listener = new udp_socket$.UDPSocketListenerPtr();
  };
  DirectSocketsService_OpenUdpSocket_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DirectSocketsService_OpenUdpSocket_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 32}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenUdpSocket_Params.options
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, DirectSocketOptions, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenUdpSocket_Params.receiver
    err = messageValidator.validateInterfaceRequest(offset + codec.kStructHeaderSize + 8, false)
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenUdpSocket_Params.listener
    err = messageValidator.validateInterface(offset + codec.kStructHeaderSize + 12, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  DirectSocketsService_OpenUdpSocket_Params.encodedSize = codec.kStructHeaderSize + 24;

  DirectSocketsService_OpenUdpSocket_Params.decode = function(decoder) {
    var packed;
    var val = new DirectSocketsService_OpenUdpSocket_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.options =
        decoder.decodeStructPointer(DirectSocketOptions);
    val.receiver =
        decoder.decodeStruct(codec.InterfaceRequest);
    val.listener =
        decoder.decodeStruct(new codec.NullableInterface(udp_socket$.UDPSocketListenerPtr));
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  DirectSocketsService_OpenUdpSocket_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DirectSocketsService_OpenUdpSocket_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(DirectSocketOptions, val.options);
    encoder.encodeStruct(codec.InterfaceRequest, val.receiver);
    encoder.encodeStruct(new codec.NullableInterface(udp_socket$.UDPSocketListenerPtr), val.listener);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function DirectSocketsService_OpenUdpSocket_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DirectSocketsService_OpenUdpSocket_ResponseParams.prototype.initDefaults_ = function() {
    this.result = 0;
    this.localAddr = null;
    this.peerAddr = null;
  };
  DirectSocketsService_OpenUdpSocket_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DirectSocketsService_OpenUdpSocket_ResponseParams.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 32}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;



    // validate DirectSocketsService_OpenUdpSocket_ResponseParams.localAddr
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 8, ip_endpoint$.IPEndPoint, true);
    if (err !== validator.validationError.NONE)
        return err;


    // validate DirectSocketsService_OpenUdpSocket_ResponseParams.peerAddr
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 16, ip_endpoint$.IPEndPoint, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  DirectSocketsService_OpenUdpSocket_ResponseParams.encodedSize = codec.kStructHeaderSize + 24;

  DirectSocketsService_OpenUdpSocket_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new DirectSocketsService_OpenUdpSocket_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.result =
        decoder.decodeStruct(codec.Int32);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.localAddr =
        decoder.decodeStructPointer(ip_endpoint$.IPEndPoint);
    val.peerAddr =
        decoder.decodeStructPointer(ip_endpoint$.IPEndPoint);
    return val;
  };

  DirectSocketsService_OpenUdpSocket_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DirectSocketsService_OpenUdpSocket_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.result);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeStructPointer(ip_endpoint$.IPEndPoint, val.localAddr);
    encoder.encodeStructPointer(ip_endpoint$.IPEndPoint, val.peerAddr);
  };
  var kDirectSocketsService_OpenTcpSocket_Name = 0;
  var kDirectSocketsService_OpenUdpSocket_Name = 1;

  function DirectSocketsServicePtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(DirectSocketsService,
                                                   handleOrPtrInfo);
  }

  function DirectSocketsServiceAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        DirectSocketsService, associatedInterfacePtrInfo);
  }

  DirectSocketsServiceAssociatedPtr.prototype =
      Object.create(DirectSocketsServicePtr.prototype);
  DirectSocketsServiceAssociatedPtr.prototype.constructor =
      DirectSocketsServiceAssociatedPtr;

  function DirectSocketsServiceProxy(receiver) {
    this.receiver_ = receiver;
  }
  DirectSocketsServicePtr.prototype.openTcpSocket = function() {
    return DirectSocketsServiceProxy.prototype.openTcpSocket
        .apply(this.ptr.getProxy(), arguments);
  };

  DirectSocketsServiceProxy.prototype.openTcpSocket = function(options, trafficAnnotation, receiver, observer) {
    var params_ = new DirectSocketsService_OpenTcpSocket_Params();
    params_.options = options;
    params_.trafficAnnotation = trafficAnnotation;
    params_.receiver = receiver;
    params_.observer = observer;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kDirectSocketsService_OpenTcpSocket_Name,
          codec.align(DirectSocketsService_OpenTcpSocket_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(DirectSocketsService_OpenTcpSocket_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(DirectSocketsService_OpenTcpSocket_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };
  DirectSocketsServicePtr.prototype.openUdpSocket = function() {
    return DirectSocketsServiceProxy.prototype.openUdpSocket
        .apply(this.ptr.getProxy(), arguments);
  };

  DirectSocketsServiceProxy.prototype.openUdpSocket = function(options, receiver, listener) {
    var params_ = new DirectSocketsService_OpenUdpSocket_Params();
    params_.options = options;
    params_.receiver = receiver;
    params_.listener = listener;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kDirectSocketsService_OpenUdpSocket_Name,
          codec.align(DirectSocketsService_OpenUdpSocket_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(DirectSocketsService_OpenUdpSocket_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(DirectSocketsService_OpenUdpSocket_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function DirectSocketsServiceStub(delegate) {
    this.delegate_ = delegate;
  }
  DirectSocketsServiceStub.prototype.openTcpSocket = function(options, trafficAnnotation, receiver, observer) {
    return this.delegate_ && this.delegate_.openTcpSocket && this.delegate_.openTcpSocket(options, trafficAnnotation, receiver, observer);
  }
  DirectSocketsServiceStub.prototype.openUdpSocket = function(options, receiver, listener) {
    return this.delegate_ && this.delegate_.openUdpSocket && this.delegate_.openUdpSocket(options, receiver, listener);
  }

  DirectSocketsServiceStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  DirectSocketsServiceStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kDirectSocketsService_OpenTcpSocket_Name:
      var params = reader.decodeStruct(DirectSocketsService_OpenTcpSocket_Params);
      this.openTcpSocket(params.options, params.trafficAnnotation, params.receiver, params.observer).then(function(response) {
        var responseParams =
            new DirectSocketsService_OpenTcpSocket_ResponseParams();
        responseParams.result = response.result;
        responseParams.localAddr = response.localAddr;
        responseParams.peerAddr = response.peerAddr;
        responseParams.receiveStream = response.receiveStream;
        responseParams.sendStream = response.sendStream;
        var builder = new codec.MessageV1Builder(
            kDirectSocketsService_OpenTcpSocket_Name,
            codec.align(DirectSocketsService_OpenTcpSocket_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(DirectSocketsService_OpenTcpSocket_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    case kDirectSocketsService_OpenUdpSocket_Name:
      var params = reader.decodeStruct(DirectSocketsService_OpenUdpSocket_Params);
      this.openUdpSocket(params.options, params.receiver, params.listener).then(function(response) {
        var responseParams =
            new DirectSocketsService_OpenUdpSocket_ResponseParams();
        responseParams.result = response.result;
        responseParams.localAddr = response.localAddr;
        responseParams.peerAddr = response.peerAddr;
        var builder = new codec.MessageV1Builder(
            kDirectSocketsService_OpenUdpSocket_Name,
            codec.align(DirectSocketsService_OpenUdpSocket_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(DirectSocketsService_OpenUdpSocket_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validateDirectSocketsServiceRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kDirectSocketsService_OpenTcpSocket_Name:
        if (message.expectsResponse())
          paramsClass = DirectSocketsService_OpenTcpSocket_Params;
      break;
      case kDirectSocketsService_OpenUdpSocket_Name:
        if (message.expectsResponse())
          paramsClass = DirectSocketsService_OpenUdpSocket_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateDirectSocketsServiceResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kDirectSocketsService_OpenTcpSocket_Name:
        if (message.isResponse())
          paramsClass = DirectSocketsService_OpenTcpSocket_ResponseParams;
        break;
      case kDirectSocketsService_OpenUdpSocket_Name:
        if (message.isResponse())
          paramsClass = DirectSocketsService_OpenUdpSocket_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var DirectSocketsService = {
    name: 'blink.mojom.DirectSocketsService',
    kVersion: 0,
    ptrClass: DirectSocketsServicePtr,
    proxyClass: DirectSocketsServiceProxy,
    stubClass: DirectSocketsServiceStub,
    validateRequest: validateDirectSocketsServiceRequest,
    validateResponse: validateDirectSocketsServiceResponse,
  };
  DirectSocketsServiceStub.prototype.validator = validateDirectSocketsServiceRequest;
  DirectSocketsServiceProxy.prototype.validator = validateDirectSocketsServiceResponse;
  exports.DirectSocketOptions = DirectSocketOptions;
  exports.DirectSocketsService = DirectSocketsService;
  exports.DirectSocketsServicePtr = DirectSocketsServicePtr;
  exports.DirectSocketsServiceAssociatedPtr = DirectSocketsServiceAssociatedPtr;
})();