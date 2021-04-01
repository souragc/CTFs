// services/data_decoder/public/mojom/resource_snapshot_for_web_bundle.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'services/data_decoder/public/mojom/resource_snapshot_for_web_bundle.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('dataDecoder.mojom');
  var big_buffer$ =
      mojo.internal.exposeNamespace('mojoBase.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'mojo/public/mojom/base/big_buffer.mojom', '../../../../mojo/public/mojom/base/big_buffer.mojom.js');
  }
  var url$ =
      mojo.internal.exposeNamespace('url.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'url/mojom/url.mojom', '../../../../url/mojom/url.mojom.js');
  }



  function SerializedResourceInfo(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  SerializedResourceInfo.prototype.initDefaults_ = function() {
    this.url = null;
    this.mimeType = null;
    this.size = 0;
  };
  SerializedResourceInfo.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  SerializedResourceInfo.validate = function(messageValidator, offset) {
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


    // validate SerializedResourceInfo.url
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, url$.Url, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate SerializedResourceInfo.mimeType
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 8, false)
    if (err !== validator.validationError.NONE)
        return err;


    return validator.validationError.NONE;
  };

  SerializedResourceInfo.encodedSize = codec.kStructHeaderSize + 24;

  SerializedResourceInfo.decode = function(decoder) {
    var packed;
    var val = new SerializedResourceInfo();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.url =
        decoder.decodeStructPointer(url$.Url);
    val.mimeType =
        decoder.decodeStruct(codec.String);
    val.size =
        decoder.decodeStruct(codec.Uint64);
    return val;
  };

  SerializedResourceInfo.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(SerializedResourceInfo.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(url$.Url, val.url);
    encoder.encodeStruct(codec.String, val.mimeType);
    encoder.encodeStruct(codec.Uint64, val.size);
  };
  function ResourceSnapshotForWebBundle_GetResourceCount_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceCount_Params.prototype.initDefaults_ = function() {
  };
  ResourceSnapshotForWebBundle_GetResourceCount_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceCount_Params.validate = function(messageValidator, offset) {
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

  ResourceSnapshotForWebBundle_GetResourceCount_Params.encodedSize = codec.kStructHeaderSize + 0;

  ResourceSnapshotForWebBundle_GetResourceCount_Params.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceCount_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceCount_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceCount_Params.encodedSize);
    encoder.writeUint32(0);
  };
  function ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.prototype.initDefaults_ = function() {
    this.count = 0;
  };
  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.count =
        decoder.decodeStruct(codec.Uint64);
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Uint64, val.count);
  };
  function ResourceSnapshotForWebBundle_GetResourceInfo_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceInfo_Params.prototype.initDefaults_ = function() {
    this.index = 0;
  };
  ResourceSnapshotForWebBundle_GetResourceInfo_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_Params.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_Params.encodedSize = codec.kStructHeaderSize + 8;

  ResourceSnapshotForWebBundle_GetResourceInfo_Params.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceInfo_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.index =
        decoder.decodeStruct(codec.Uint64);
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceInfo_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Uint64, val.index);
  };
  function ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.prototype.initDefaults_ = function() {
    this.info = null;
  };
  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.validate = function(messageValidator, offset) {
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


    // validate ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.info
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, SerializedResourceInfo, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.info =
        decoder.decodeStructPointer(SerializedResourceInfo);
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(SerializedResourceInfo, val.info);
  };
  function ResourceSnapshotForWebBundle_GetResourceBody_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceBody_Params.prototype.initDefaults_ = function() {
    this.index = 0;
  };
  ResourceSnapshotForWebBundle_GetResourceBody_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceBody_Params.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  ResourceSnapshotForWebBundle_GetResourceBody_Params.encodedSize = codec.kStructHeaderSize + 8;

  ResourceSnapshotForWebBundle_GetResourceBody_Params.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceBody_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.index =
        decoder.decodeStruct(codec.Uint64);
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceBody_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceBody_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Uint64, val.index);
  };
  function ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.prototype.initDefaults_ = function() {
    this.data = null;
  };
  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 24}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.data
    err = messageValidator.validateUnion(offset + codec.kStructHeaderSize + 0, big_buffer$.BigBuffer, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.encodedSize = codec.kStructHeaderSize + 16;

  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.data =
        decoder.decodeStruct(big_buffer$.BigBuffer);
    return val;
  };

  ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(big_buffer$.BigBuffer, val.data);
  };
  var kResourceSnapshotForWebBundle_GetResourceCount_Name = 818845371;
  var kResourceSnapshotForWebBundle_GetResourceInfo_Name = 463404438;
  var kResourceSnapshotForWebBundle_GetResourceBody_Name = 1584378499;

  function ResourceSnapshotForWebBundlePtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(ResourceSnapshotForWebBundle,
                                                   handleOrPtrInfo);
  }

  function ResourceSnapshotForWebBundleAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        ResourceSnapshotForWebBundle, associatedInterfacePtrInfo);
  }

  ResourceSnapshotForWebBundleAssociatedPtr.prototype =
      Object.create(ResourceSnapshotForWebBundlePtr.prototype);
  ResourceSnapshotForWebBundleAssociatedPtr.prototype.constructor =
      ResourceSnapshotForWebBundleAssociatedPtr;

  function ResourceSnapshotForWebBundleProxy(receiver) {
    this.receiver_ = receiver;
  }
  ResourceSnapshotForWebBundlePtr.prototype.getResourceCount = function() {
    return ResourceSnapshotForWebBundleProxy.prototype.getResourceCount
        .apply(this.ptr.getProxy(), arguments);
  };

  ResourceSnapshotForWebBundleProxy.prototype.getResourceCount = function() {
    var params_ = new ResourceSnapshotForWebBundle_GetResourceCount_Params();
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kResourceSnapshotForWebBundle_GetResourceCount_Name,
          codec.align(ResourceSnapshotForWebBundle_GetResourceCount_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceCount_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };
  ResourceSnapshotForWebBundlePtr.prototype.getResourceInfo = function() {
    return ResourceSnapshotForWebBundleProxy.prototype.getResourceInfo
        .apply(this.ptr.getProxy(), arguments);
  };

  ResourceSnapshotForWebBundleProxy.prototype.getResourceInfo = function(index) {
    var params_ = new ResourceSnapshotForWebBundle_GetResourceInfo_Params();
    params_.index = index;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kResourceSnapshotForWebBundle_GetResourceInfo_Name,
          codec.align(ResourceSnapshotForWebBundle_GetResourceInfo_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceInfo_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };
  ResourceSnapshotForWebBundlePtr.prototype.getResourceBody = function() {
    return ResourceSnapshotForWebBundleProxy.prototype.getResourceBody
        .apply(this.ptr.getProxy(), arguments);
  };

  ResourceSnapshotForWebBundleProxy.prototype.getResourceBody = function(index) {
    var params_ = new ResourceSnapshotForWebBundle_GetResourceBody_Params();
    params_.index = index;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kResourceSnapshotForWebBundle_GetResourceBody_Name,
          codec.align(ResourceSnapshotForWebBundle_GetResourceBody_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceBody_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function ResourceSnapshotForWebBundleStub(delegate) {
    this.delegate_ = delegate;
  }
  ResourceSnapshotForWebBundleStub.prototype.getResourceCount = function() {
    return this.delegate_ && this.delegate_.getResourceCount && this.delegate_.getResourceCount();
  }
  ResourceSnapshotForWebBundleStub.prototype.getResourceInfo = function(index) {
    return this.delegate_ && this.delegate_.getResourceInfo && this.delegate_.getResourceInfo(index);
  }
  ResourceSnapshotForWebBundleStub.prototype.getResourceBody = function(index) {
    return this.delegate_ && this.delegate_.getResourceBody && this.delegate_.getResourceBody(index);
  }

  ResourceSnapshotForWebBundleStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  ResourceSnapshotForWebBundleStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kResourceSnapshotForWebBundle_GetResourceCount_Name:
      var params = reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceCount_Params);
      this.getResourceCount().then(function(response) {
        var responseParams =
            new ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams();
        responseParams.count = response.count;
        var builder = new codec.MessageV1Builder(
            kResourceSnapshotForWebBundle_GetResourceCount_Name,
            codec.align(ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    case kResourceSnapshotForWebBundle_GetResourceInfo_Name:
      var params = reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceInfo_Params);
      this.getResourceInfo(params.index).then(function(response) {
        var responseParams =
            new ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams();
        responseParams.info = response.info;
        var builder = new codec.MessageV1Builder(
            kResourceSnapshotForWebBundle_GetResourceInfo_Name,
            codec.align(ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    case kResourceSnapshotForWebBundle_GetResourceBody_Name:
      var params = reader.decodeStruct(ResourceSnapshotForWebBundle_GetResourceBody_Params);
      this.getResourceBody(params.index).then(function(response) {
        var responseParams =
            new ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams();
        responseParams.data = response.data;
        var builder = new codec.MessageV1Builder(
            kResourceSnapshotForWebBundle_GetResourceBody_Name,
            codec.align(ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validateResourceSnapshotForWebBundleRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kResourceSnapshotForWebBundle_GetResourceCount_Name:
        if (message.expectsResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceCount_Params;
      break;
      case kResourceSnapshotForWebBundle_GetResourceInfo_Name:
        if (message.expectsResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceInfo_Params;
      break;
      case kResourceSnapshotForWebBundle_GetResourceBody_Name:
        if (message.expectsResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceBody_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateResourceSnapshotForWebBundleResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kResourceSnapshotForWebBundle_GetResourceCount_Name:
        if (message.isResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceCount_ResponseParams;
        break;
      case kResourceSnapshotForWebBundle_GetResourceInfo_Name:
        if (message.isResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceInfo_ResponseParams;
        break;
      case kResourceSnapshotForWebBundle_GetResourceBody_Name:
        if (message.isResponse())
          paramsClass = ResourceSnapshotForWebBundle_GetResourceBody_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var ResourceSnapshotForWebBundle = {
    name: 'data_decoder.mojom.ResourceSnapshotForWebBundle',
    kVersion: 0,
    ptrClass: ResourceSnapshotForWebBundlePtr,
    proxyClass: ResourceSnapshotForWebBundleProxy,
    stubClass: ResourceSnapshotForWebBundleStub,
    validateRequest: validateResourceSnapshotForWebBundleRequest,
    validateResponse: validateResourceSnapshotForWebBundleResponse,
  };
  ResourceSnapshotForWebBundleStub.prototype.validator = validateResourceSnapshotForWebBundleRequest;
  ResourceSnapshotForWebBundleProxy.prototype.validator = validateResourceSnapshotForWebBundleResponse;
  exports.SerializedResourceInfo = SerializedResourceInfo;
  exports.ResourceSnapshotForWebBundle = ResourceSnapshotForWebBundle;
  exports.ResourceSnapshotForWebBundlePtr = ResourceSnapshotForWebBundlePtr;
  exports.ResourceSnapshotForWebBundleAssociatedPtr = ResourceSnapshotForWebBundleAssociatedPtr;
})();