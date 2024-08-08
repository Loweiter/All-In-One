# 下载安装

```
curl -O https://arthas.aliyun.com/arthas-boot.jar && java -jar arthas-boot.jar

```

# Trace

```
trace com.libra.feature.controller.FeatureController getFeaturePage '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "7a1d0b00-8640-4227-b66a-10ca1ad1abe1"'

trace com.libra.empower.service.impl.EmpowerUpdateServiceImpl checkVersion '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "3372888e-2246-40ca-aac9-be3e87ab4029" && params.length > 4'

trace libra.common.service.ServiceFilter itemCheckBeanAndSourceResult  -n 5 --skipJDKMethod false 
```
```
trace com.libra.feature.* *  -n 1 --skipJDKMethod true 
```

# Watch

```
watch com.libra.feature.service.impl.FeatureServiceImpl sortFeatureList  'returnObj.featureList' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "b7d5d38d-9a23-4777-a9d9-a49ebbec58f1" && params[0].tabId == 80' -n 1  -x 3 
```
watch com.libra.recommend.localcache.ServiceConfigureLocalCache getConfigObject '{@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams(),returnObj}' 'params[0]=="AROfferCpNums"'  -n 2  -x 3
watch com.libra.recommend.localcache.ServiceConfigureLocalCache getConfigObject '{params,returnObj,throwExp}'  'params[0]=="AROfferCpNums"'  -n 2  -x 1
trace com.libra.recommend.localcache.ServiceConfigureLocalCache getConfigObject 'params[0]=="AROfferCpNums"' -n 5
watch com.google.common.collect.Maps$AsMapView get '{params,returnObj,throwExp}'  'params[0]=="AROfferCpNums"' -n 5  -x 3
watch java.util.HashMap get '{params,returnObj,throwExp}' 'params[0]=="AROfferCpNums"' -n 5  -x 3
watch com.libra.feature.service.impl.feature.RankFeatureHandler getDataCenterFeature 'returnObj' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "b7d5d38d-9a23-4777-a9d9-a49ebbec58f1"' -n 1  -x 3

trace com.libra.recommend.service.impl.InstallServiceImpl groupRecommend '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"' -n 1
watch com.libra.recommend.convert.InstallConvert getOneKeyInstallDTOFromItem  'returnObj' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"' -n 1 -x 3
watch com.libra.recommend.localcache.InstallGroupRecLocalCache getData 'returnObj' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"' -n 1 -x 3

trace com.libra.recommend.service.impl.InstallServiceImpl buildResult  '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"&&params[1].groupId==12' -n 1

trace com.libra.recommend.service.impl.ItemServiceImpl buildInstallDTO '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"' -n 1

watch com.libra.recommend.service.impl.InstallServiceImpl mergeByLocationForGroupRecommend 'params[0].commonRecList' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"'  -n 1  -x 3  
trace com.libra.recommend.service.impl.InstallServiceImpl mergeByLocationForGroupRecommend  '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().getGaid() == "ebdc119c-b7e8-4048-8db7-c60de870a4323234"'  -n 1
watch com.libra.feature.controller.FeatureController queryNavType '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().countryCode' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().countryCode != "RU"'  -n 10  -x 3
watch com.libra.feature.controller.FeatureController queryNavType '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams()' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().gaid=="86f50ff6-5c3d-4e89-a9c5-efb560c1998e"'  -n 1  -x 3
watch libra.domain.device.client.impl.FeatureClientImpl queryNavType '@libra.common.protocol.context.LocalRequestContextHolder@getLocalRequestContext().getAllParamsMap()' '@libra.common.protocol.context.LocalRequestContextHolder@getLocalReqCommonParams().gaid=="86f50ff6-5c3d-4e89-a9c5-efb560c1998e"'  -n 1  -x 3