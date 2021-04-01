// media/mojo/mojom/renderer_extensions.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'media/mojo/mojom/renderer_extensions.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('media.mojom');
  var media_types$ =
      mojo.internal.exposeNamespace('media.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'media/mojo/mojom/media_types.mojom', 'media_types.mojom.js');
  }
  var time$ =
      mojo.internal.exposeNamespace('mojoBase.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'mojo/public/mojom/base/time.mojom', '../../../mojo/public/mojom/base/time.mojom.js');
  }
  var unguessable_token$ =
      mojo.internal.exposeNamespace('mojoBase.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'mojo/public/mojom/base/unguessable_token.mojom', '../../../mojo/public/mojom/base/unguessable_token.mojom.js');
  }
  var geometry$ =
      mojo.internal.exposeNamespace('gfx.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'ui/gfx/geometry/mojom/geometry.mojom', '../../../ui/gfx/geometry/mojom/geometry.mojom.js');
  }



  function MediaPlayerRendererClientExtension_OnVideoSizeChange_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.prototype.initDefaults_ = function() {
    this.size = null;
  };
  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.size
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, geometry$.Size, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.encodedSize = codec.kStructHeaderSize + 8;

  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.decode = function(decoder) {
    var packed;
    var val = new MediaPlayerRendererClientExtension_OnVideoSizeChange_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.size =
        decoder.decodeStructPointer(geometry$.Size);
    return val;
  };

  MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(geometry$.Size, val.size);
  };
  function MediaPlayerRendererClientExtension_OnDurationChange_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  MediaPlayerRendererClientExtension_OnDurationChange_Params.prototype.initDefaults_ = function() {
    this.duration = null;
  };
  MediaPlayerRendererClientExtension_OnDurationChange_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  MediaPlayerRendererClientExtension_OnDurationChange_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate MediaPlayerRendererClientExtension_OnDurationChange_Params.duration
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, time$.TimeDelta, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  MediaPlayerRendererClientExtension_OnDurationChange_Params.encodedSize = codec.kStructHeaderSize + 8;

  MediaPlayerRendererClientExtension_OnDurationChange_Params.decode = function(decoder) {
    var packed;
    var val = new MediaPlayerRendererClientExtension_OnDurationChange_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.duration =
        decoder.decodeStructPointer(time$.TimeDelta);
    return val;
  };

  MediaPlayerRendererClientExtension_OnDurationChange_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(MediaPlayerRendererClientExtension_OnDurationChange_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(time$.TimeDelta, val.duration);
  };
  function MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.prototype.initDefaults_ = function() {
  };
  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 8}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.encodedSize = codec.kStructHeaderSize + 0;

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.decode = function(decoder) {
    var packed;
    var val = new MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    return val;
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.encodedSize);
    encoder.writeUint32(0);
  };
  function MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.prototype.initDefaults_ = function() {
    this.requestToken = null;
  };
  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.requestToken
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, unguessable_token$.UnguessableToken, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.requestToken =
        decoder.decodeStructPointer(unguessable_token$.UnguessableToken);
    return val;
  };

  MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(unguessable_token$.UnguessableToken, val.requestToken);
  };
  function FlingingRendererClientExtension_OnRemotePlayStateChange_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.prototype.initDefaults_ = function() {
    this.state = 0;
  };
  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate FlingingRendererClientExtension_OnRemotePlayStateChange_Params.state
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 0, media_types$.MediaStatusState);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.encodedSize = codec.kStructHeaderSize + 8;

  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.decode = function(decoder) {
    var packed;
    var val = new FlingingRendererClientExtension_OnRemotePlayStateChange_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.state =
        decoder.decodeStruct(codec.Int32);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  FlingingRendererClientExtension_OnRemotePlayStateChange_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(FlingingRendererClientExtension_OnRemotePlayStateChange_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.state);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  var kMediaPlayerRendererClientExtension_OnVideoSizeChange_Name = 1624261124;
  var kMediaPlayerRendererClientExtension_OnDurationChange_Name = 992457420;

  function MediaPlayerRendererClientExtensionPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(MediaPlayerRendererClientExtension,
                                                   handleOrPtrInfo);
  }

  function MediaPlayerRendererClientExtensionAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        MediaPlayerRendererClientExtension, associatedInterfacePtrInfo);
  }

  MediaPlayerRendererClientExtensionAssociatedPtr.prototype =
      Object.create(MediaPlayerRendererClientExtensionPtr.prototype);
  MediaPlayerRendererClientExtensionAssociatedPtr.prototype.constructor =
      MediaPlayerRendererClientExtensionAssociatedPtr;

  function MediaPlayerRendererClientExtensionProxy(receiver) {
    this.receiver_ = receiver;
  }
  MediaPlayerRendererClientExtensionPtr.prototype.onVideoSizeChange = function() {
    return MediaPlayerRendererClientExtensionProxy.prototype.onVideoSizeChange
        .apply(this.ptr.getProxy(), arguments);
  };

  MediaPlayerRendererClientExtensionProxy.prototype.onVideoSizeChange = function(size) {
    var params_ = new MediaPlayerRendererClientExtension_OnVideoSizeChange_Params();
    params_.size = size;
    var builder = new codec.MessageV0Builder(
        kMediaPlayerRendererClientExtension_OnVideoSizeChange_Name,
        codec.align(MediaPlayerRendererClientExtension_OnVideoSizeChange_Params.encodedSize));
    builder.encodeStruct(MediaPlayerRendererClientExtension_OnVideoSizeChange_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };
  MediaPlayerRendererClientExtensionPtr.prototype.onDurationChange = function() {
    return MediaPlayerRendererClientExtensionProxy.prototype.onDurationChange
        .apply(this.ptr.getProxy(), arguments);
  };

  MediaPlayerRendererClientExtensionProxy.prototype.onDurationChange = function(duration) {
    var params_ = new MediaPlayerRendererClientExtension_OnDurationChange_Params();
    params_.duration = duration;
    var builder = new codec.MessageV0Builder(
        kMediaPlayerRendererClientExtension_OnDurationChange_Name,
        codec.align(MediaPlayerRendererClientExtension_OnDurationChange_Params.encodedSize));
    builder.encodeStruct(MediaPlayerRendererClientExtension_OnDurationChange_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };

  function MediaPlayerRendererClientExtensionStub(delegate) {
    this.delegate_ = delegate;
  }
  MediaPlayerRendererClientExtensionStub.prototype.onVideoSizeChange = function(size) {
    return this.delegate_ && this.delegate_.onVideoSizeChange && this.delegate_.onVideoSizeChange(size);
  }
  MediaPlayerRendererClientExtensionStub.prototype.onDurationChange = function(duration) {
    return this.delegate_ && this.delegate_.onDurationChange && this.delegate_.onDurationChange(duration);
  }

  MediaPlayerRendererClientExtensionStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kMediaPlayerRendererClientExtension_OnVideoSizeChange_Name:
      var params = reader.decodeStruct(MediaPlayerRendererClientExtension_OnVideoSizeChange_Params);
      this.onVideoSizeChange(params.size);
      return true;
    case kMediaPlayerRendererClientExtension_OnDurationChange_Name:
      var params = reader.decodeStruct(MediaPlayerRendererClientExtension_OnDurationChange_Params);
      this.onDurationChange(params.duration);
      return true;
    default:
      return false;
    }
  };

  MediaPlayerRendererClientExtensionStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  function validateMediaPlayerRendererClientExtensionRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kMediaPlayerRendererClientExtension_OnVideoSizeChange_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = MediaPlayerRendererClientExtension_OnVideoSizeChange_Params;
      break;
      case kMediaPlayerRendererClientExtension_OnDurationChange_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = MediaPlayerRendererClientExtension_OnDurationChange_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateMediaPlayerRendererClientExtensionResponse(messageValidator) {
    return validator.validationError.NONE;
  }

  var MediaPlayerRendererClientExtension = {
    name: 'media.mojom.MediaPlayerRendererClientExtension',
    kVersion: 0,
    ptrClass: MediaPlayerRendererClientExtensionPtr,
    proxyClass: MediaPlayerRendererClientExtensionProxy,
    stubClass: MediaPlayerRendererClientExtensionStub,
    validateRequest: validateMediaPlayerRendererClientExtensionRequest,
    validateResponse: null,
  };
  MediaPlayerRendererClientExtensionStub.prototype.validator = validateMediaPlayerRendererClientExtensionRequest;
  MediaPlayerRendererClientExtensionProxy.prototype.validator = null;
  var kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name = 1253159992;

  function MediaPlayerRendererExtensionPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(MediaPlayerRendererExtension,
                                                   handleOrPtrInfo);
  }

  function MediaPlayerRendererExtensionAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        MediaPlayerRendererExtension, associatedInterfacePtrInfo);
  }

  MediaPlayerRendererExtensionAssociatedPtr.prototype =
      Object.create(MediaPlayerRendererExtensionPtr.prototype);
  MediaPlayerRendererExtensionAssociatedPtr.prototype.constructor =
      MediaPlayerRendererExtensionAssociatedPtr;

  function MediaPlayerRendererExtensionProxy(receiver) {
    this.receiver_ = receiver;
  }
  MediaPlayerRendererExtensionPtr.prototype.initiateScopedSurfaceRequest = function() {
    return MediaPlayerRendererExtensionProxy.prototype.initiateScopedSurfaceRequest
        .apply(this.ptr.getProxy(), arguments);
  };

  MediaPlayerRendererExtensionProxy.prototype.initiateScopedSurfaceRequest = function() {
    var params_ = new MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params();
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name,
          codec.align(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function MediaPlayerRendererExtensionStub(delegate) {
    this.delegate_ = delegate;
  }
  MediaPlayerRendererExtensionStub.prototype.initiateScopedSurfaceRequest = function() {
    return this.delegate_ && this.delegate_.initiateScopedSurfaceRequest && this.delegate_.initiateScopedSurfaceRequest();
  }

  MediaPlayerRendererExtensionStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  MediaPlayerRendererExtensionStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name:
      var params = reader.decodeStruct(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params);
      this.initiateScopedSurfaceRequest().then(function(response) {
        var responseParams =
            new MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams();
        responseParams.requestToken = response.requestToken;
        var builder = new codec.MessageV1Builder(
            kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name,
            codec.align(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validateMediaPlayerRendererExtensionRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name:
        if (message.expectsResponse())
          paramsClass = MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateMediaPlayerRendererExtensionResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kMediaPlayerRendererExtension_InitiateScopedSurfaceRequest_Name:
        if (message.isResponse())
          paramsClass = MediaPlayerRendererExtension_InitiateScopedSurfaceRequest_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var MediaPlayerRendererExtension = {
    name: 'media.mojom.MediaPlayerRendererExtension',
    kVersion: 0,
    ptrClass: MediaPlayerRendererExtensionPtr,
    proxyClass: MediaPlayerRendererExtensionProxy,
    stubClass: MediaPlayerRendererExtensionStub,
    validateRequest: validateMediaPlayerRendererExtensionRequest,
    validateResponse: validateMediaPlayerRendererExtensionResponse,
  };
  MediaPlayerRendererExtensionStub.prototype.validator = validateMediaPlayerRendererExtensionRequest;
  MediaPlayerRendererExtensionProxy.prototype.validator = validateMediaPlayerRendererExtensionResponse;
  var kFlingingRendererClientExtension_OnRemotePlayStateChange_Name = 1923005743;

  function FlingingRendererClientExtensionPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(FlingingRendererClientExtension,
                                                   handleOrPtrInfo);
  }

  function FlingingRendererClientExtensionAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        FlingingRendererClientExtension, associatedInterfacePtrInfo);
  }

  FlingingRendererClientExtensionAssociatedPtr.prototype =
      Object.create(FlingingRendererClientExtensionPtr.prototype);
  FlingingRendererClientExtensionAssociatedPtr.prototype.constructor =
      FlingingRendererClientExtensionAssociatedPtr;

  function FlingingRendererClientExtensionProxy(receiver) {
    this.receiver_ = receiver;
  }
  FlingingRendererClientExtensionPtr.prototype.onRemotePlayStateChange = function() {
    return FlingingRendererClientExtensionProxy.prototype.onRemotePlayStateChange
        .apply(this.ptr.getProxy(), arguments);
  };

  FlingingRendererClientExtensionProxy.prototype.onRemotePlayStateChange = function(state) {
    var params_ = new FlingingRendererClientExtension_OnRemotePlayStateChange_Params();
    params_.state = state;
    var builder = new codec.MessageV0Builder(
        kFlingingRendererClientExtension_OnRemotePlayStateChange_Name,
        codec.align(FlingingRendererClientExtension_OnRemotePlayStateChange_Params.encodedSize));
    builder.encodeStruct(FlingingRendererClientExtension_OnRemotePlayStateChange_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };

  function FlingingRendererClientExtensionStub(delegate) {
    this.delegate_ = delegate;
  }
  FlingingRendererClientExtensionStub.prototype.onRemotePlayStateChange = function(state) {
    return this.delegate_ && this.delegate_.onRemotePlayStateChange && this.delegate_.onRemotePlayStateChange(state);
  }

  FlingingRendererClientExtensionStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kFlingingRendererClientExtension_OnRemotePlayStateChange_Name:
      var params = reader.decodeStruct(FlingingRendererClientExtension_OnRemotePlayStateChange_Params);
      this.onRemotePlayStateChange(params.state);
      return true;
    default:
      return false;
    }
  };

  FlingingRendererClientExtensionStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  function validateFlingingRendererClientExtensionRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kFlingingRendererClientExtension_OnRemotePlayStateChange_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = FlingingRendererClientExtension_OnRemotePlayStateChange_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateFlingingRendererClientExtensionResponse(messageValidator) {
    return validator.validationError.NONE;
  }

  var FlingingRendererClientExtension = {
    name: 'media.mojom.FlingingRendererClientExtension',
    kVersion: 0,
    ptrClass: FlingingRendererClientExtensionPtr,
    proxyClass: FlingingRendererClientExtensionProxy,
    stubClass: FlingingRendererClientExtensionStub,
    validateRequest: validateFlingingRendererClientExtensionRequest,
    validateResponse: null,
  };
  FlingingRendererClientExtensionStub.prototype.validator = validateFlingingRendererClientExtensionRequest;
  FlingingRendererClientExtensionProxy.prototype.validator = null;
  exports.MediaPlayerRendererClientExtension = MediaPlayerRendererClientExtension;
  exports.MediaPlayerRendererClientExtensionPtr = MediaPlayerRendererClientExtensionPtr;
  exports.MediaPlayerRendererClientExtensionAssociatedPtr = MediaPlayerRendererClientExtensionAssociatedPtr;
  exports.MediaPlayerRendererExtension = MediaPlayerRendererExtension;
  exports.MediaPlayerRendererExtensionPtr = MediaPlayerRendererExtensionPtr;
  exports.MediaPlayerRendererExtensionAssociatedPtr = MediaPlayerRendererExtensionAssociatedPtr;
  exports.FlingingRendererClientExtension = FlingingRendererClientExtension;
  exports.FlingingRendererClientExtensionPtr = FlingingRendererClientExtensionPtr;
  exports.FlingingRendererClientExtensionAssociatedPtr = FlingingRendererClientExtensionAssociatedPtr;
})();