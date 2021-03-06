// media/mojo/mojom/display_media_information.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'media/mojo/mojom/display_media_information.mojom';
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


  var DisplayCaptureSurfaceType = {};
  DisplayCaptureSurfaceType.MONITOR = 0;
  DisplayCaptureSurfaceType.WINDOW = 1;
  DisplayCaptureSurfaceType.APPLICATION = 2;
  DisplayCaptureSurfaceType.BROWSER = 3;
  DisplayCaptureSurfaceType.MIN_VALUE = 0,
  DisplayCaptureSurfaceType.MAX_VALUE = 3,

  DisplayCaptureSurfaceType.isKnownEnumValue = function(value) {
    switch (value) {
    case 0:
    case 1:
    case 2:
    case 3:
      return true;
    }
    return false;
  };

  DisplayCaptureSurfaceType.validate = function(enumValue) {
    var isExtensible = false;
    if (isExtensible || this.isKnownEnumValue(enumValue))
      return validator.validationError.NONE;

    return validator.validationError.UNKNOWN_ENUM_VALUE;
  };
  var CursorCaptureType = {};
  CursorCaptureType.NEVER = 0;
  CursorCaptureType.ALWAYS = 1;
  CursorCaptureType.MOTION = 2;
  CursorCaptureType.MIN_VALUE = 0,
  CursorCaptureType.MAX_VALUE = 2,

  CursorCaptureType.isKnownEnumValue = function(value) {
    switch (value) {
    case 0:
    case 1:
    case 2:
      return true;
    }
    return false;
  };

  CursorCaptureType.validate = function(enumValue) {
    var isExtensible = false;
    if (isExtensible || this.isKnownEnumValue(enumValue))
      return validator.validationError.NONE;

    return validator.validationError.UNKNOWN_ENUM_VALUE;
  };

  function DisplayMediaInformation(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  DisplayMediaInformation.prototype.initDefaults_ = function() {
    this.displaySurface = 0;
    this.logicalSurface = false;
    this.cursor = 0;
  };
  DisplayMediaInformation.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  DisplayMediaInformation.validate = function(messageValidator, offset) {
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


    // validate DisplayMediaInformation.displaySurface
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 0, DisplayCaptureSurfaceType);
    if (err !== validator.validationError.NONE)
        return err;



    // validate DisplayMediaInformation.cursor
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 8, CursorCaptureType);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  DisplayMediaInformation.encodedSize = codec.kStructHeaderSize + 16;

  DisplayMediaInformation.decode = function(decoder) {
    var packed;
    var val = new DisplayMediaInformation();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.displaySurface =
        decoder.decodeStruct(codec.Int32);
    packed = decoder.readUint8();
    val.logicalSurface = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.cursor =
        decoder.decodeStruct(codec.Int32);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  DisplayMediaInformation.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(DisplayMediaInformation.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.displaySurface);
    packed = 0;
    packed |= (val.logicalSurface & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeStruct(codec.Int32, val.cursor);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  exports.DisplayCaptureSurfaceType = DisplayCaptureSurfaceType;
  exports.CursorCaptureType = CursorCaptureType;
  exports.DisplayMediaInformation = DisplayMediaInformation;
})();