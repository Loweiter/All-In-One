# 下载安装

```
curl -O https://arthas.aliyun.com/arthas-boot.jar
java -jar arthas-boot.jar
```

# Trace

```
trace com.libra.feature.controller.FeatureController getFeaturePage '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "7a1d0b00-8640-4227-b66a-10ca1ad1abe1"'

```
```
trace com.libra.feature.* *  -n 1 --skipJDKMethod true 
```

# Watch

```
watch com.libra.feature.service.impl.FeatureServiceImpl sortFeatureList  'returnObj.featureList' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "7a1d0b00-8640-4227-b66a-10ca1ad1abe1" && params[0].tabId == 80' -n 1  -x 3 
```
