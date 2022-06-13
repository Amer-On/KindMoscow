# ***API для сервиса Добрая Москва***

Нашей командой было принято решение написания *отдельного API* для вынесения отдельных функций вне самого приложения. Такое решение позволит легче интегрировать новые решения вроде мобильных приложений, которые будут очень актуальны для волонтёров, поскольку **большая** часть волонтёров является студентами. Это позволит создать единую экосистему из различных приложений и сервисов.
Тем не менее в рамках хакатона мы решили вынести лишь малую часть в API (отправка электронных писем для подтверждения регистрации или смены пароля). Решение это обусловлено тем, чтобы в дальнейшем можно было легче отказаться от использования API, если всё же будет принято решение о том, что веб приложение будет единственным решением. Тогда перенести с API на бэкэнд будет гораздо проще.
По требованию заказчика API, как и само приложение, контейнеризовано и полностью готово к эксплуатации.


# **Docker deployment**
### Docker build
> docker build -t km_api .

## Alternatively download ready for deploy image 
### Docker pull image
> docker pull 

### Docker run for tests
> docker run --rm -p 80:80 km_api

### Docker run on deployment
> docker run -d -p 80:80 --name km_api