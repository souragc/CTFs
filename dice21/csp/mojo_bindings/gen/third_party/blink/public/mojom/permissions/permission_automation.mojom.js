// third_party/blink/public/mojom/permissions/permission_automation.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/permissions/permission_automation.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('blink.test.mojom');
  var permission$ =
      mojo.internal.exposeNamespace('blink.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'third_party/blink/public/mojom/permissions/permission.mojom', 'permission.mojom.js');
  }
  var permission_status$ =
      mojo.internal.exposeNamespace('blink.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'third_party/blink/public/mojom/permissions/permission_status.mojom', 'permission_status.mojom.js');
  }
  var url$ =
      mojo.internal.exposeNamespace('url.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'url/mojom/url.mojom', '../../../../../url/mojom/url.mojom.js');
  }



  function PermissionAutomation_SetPermission_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PermissionAutomation_SetPermission_Params.prototype.initDefaults_ = function() {
    this.descriptor = null;
    this.status = 0;
    this.origin = null;
    this.embeddingOrigin = null;
  };
  PermissionAutomation_SetPermission_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PermissionAutomation_SetPermission_Params.validate = function(messageValidator, offset) {
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


    // validate PermissionAutomation_SetPermission_Params.descriptor
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, permission$.PermissionDescriptor, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate PermissionAutomation_SetPermission_Params.status
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 8, permission_status$.PermissionStatus);
    if (err !== validator.validationError.NONE)
        return err;


    // validate PermissionAutomation_SetPermission_Params.origin
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 16, url$.Url, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate PermissionAutomation_SetPermission_Params.embeddingOrigin
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 24, url$.Url, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  PermissionAutomation_SetPermission_Params.encodedSize = codec.kStructHeaderSize + 32;

  PermissionAutomation_SetPermission_Params.decode = function(decoder) {
    var packed;
    var val = new PermissionAutomation_SetPermission_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.descriptor =
        decoder.decodeStructPointer(permission$.PermissionDescriptor);
    val.status =
        decoder.decodeStruct(codec.Int32);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.origin =
        decoder.decodeStructPointer(url$.Url);
    val.embeddingOrigin =
        decoder.decodeStructPointer(url$.Url);
    return val;
  };

  PermissionAutomation_SetPermission_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PermissionAutomation_SetPermission_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(permission$.PermissionDescriptor, val.descriptor);
    encoder.encodeStruct(codec.Int32, val.status);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeStructPointer(url$.Url, val.origin);
    encoder.encodeStructPointer(url$.Url, val.embeddingOrigin);
  };
  function PermissionAutomation_SetPermission_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PermissionAutomation_SetPermission_ResponseParams.prototype.initDefaults_ = function() {
    this.success = false;
  };
  PermissionAutomation_SetPermission_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PermissionAutomation_SetPermission_ResponseParams.validate = function(messageValidator, offset) {
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

  PermissionAutomation_SetPermission_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  PermissionAutomation_SetPermission_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new PermissionAutomation_SetPermission_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    packed = decoder.readUint8();
    val.success = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  PermissionAutomation_SetPermission_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PermissionAutomation_SetPermission_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    packed = 0;
    packed |= (val.success & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  var kPermissionAutomation_SetPermission_Name = 0;

  function PermissionAutomationPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(PermissionAutomation,
                                                   handleOrPtrInfo);
  }

  function PermissionAutomationAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        PermissionAutomation, associatedInterfacePtrInfo);
  }

  PermissionAutomationAssociatedPtr.prototype =
      Object.create(PermissionAutomationPtr.prototype);
  PermissionAutomationAssociatedPtr.prototype.constructor =
      PermissionAutomationAssociatedPtr;

  function PermissionAutomationProxy(receiver) {
    this.receiver_ = receiver;
  }
  PermissionAutomationPtr.prototype.setPermission = function() {
    return PermissionAutomationProxy.prototype.setPermission
        .apply(this.ptr.getProxy(), arguments);
  };

  PermissionAutomationProxy.prototype.setPermission = function(descriptor, status, origin, embeddingOrigin) {
    var params_ = new PermissionAutomation_SetPermission_Params();
    params_.descriptor = descriptor;
    params_.status = status;
    params_.origin = origin;
    params_.embeddingOrigin = embeddingOrigin;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kPermissionAutomation_SetPermission_Name,
          codec.align(PermissionAutomation_SetPermission_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(PermissionAutomation_SetPermission_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(PermissionAutomation_SetPermission_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function PermissionAutomationStub(delegate) {
    this.delegate_ = delegate;
  }
  PermissionAutomationStub.prototype.setPermission = function(descriptor, status, origin, embeddingOrigin) {
    return this.delegate_ && this.delegate_.setPermission && this.delegate_.setPermission(descriptor, status, origin, embeddingOrigin);
  }

  PermissionAutomationStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  PermissionAutomationStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kPermissionAutomation_SetPermission_Name:
      var params = reader.decodeStruct(PermissionAutomation_SetPermission_Params);
      this.setPermission(params.descriptor, params.status, params.origin, params.embeddingOrigin).then(function(response) {
        var responseParams =
            new PermissionAutomation_SetPermission_ResponseParams();
        responseParams.success = response.success;
        var builder = new codec.MessageV1Builder(
            kPermissionAutomation_SetPermission_Name,
            codec.align(PermissionAutomation_SetPermission_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(PermissionAutomation_SetPermission_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validatePermissionAutomationRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kPermissionAutomation_SetPermission_Name:
        if (message.expectsResponse())
          paramsClass = PermissionAutomation_SetPermission_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validatePermissionAutomationResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kPermissionAutomation_SetPermission_Name:
        if (message.isResponse())
          paramsClass = PermissionAutomation_SetPermission_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var PermissionAutomation = {
    name: 'blink.test.mojom.PermissionAutomation',
    kVersion: 0,
    ptrClass: PermissionAutomationPtr,
    proxyClass: PermissionAutomationProxy,
    stubClass: PermissionAutomationStub,
    validateRequest: validatePermissionAutomationRequest,
    validateResponse: validatePermissionAutomationResponse,
  };
  PermissionAutomationStub.prototype.validator = validatePermissionAutomationRequest;
  PermissionAutomationProxy.prototype.validator = validatePermissionAutomationResponse;
  exports.PermissionAutomation = PermissionAutomation;
  exports.PermissionAutomationPtr = PermissionAutomationPtr;
  exports.PermissionAutomationAssociatedPtr = PermissionAutomationAssociatedPtr;
})();