FROM microsoft/dotnet:2.2-aspnetcore-runtime AS base
WORKDIR /app
EXPOSE 80

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY ["ScavengePad/ScavengePad.csproj", "ScavengePad/"]
COPY ["SharpReverseProxy/SharpReverseProxy.csproj", "SharpReverseProxy/"]
RUN dotnet restore "ScavengePad/ScavengePad.csproj"
COPY . .
WORKDIR "/src/ScavengePad"
RUN dotnet publish "ScavengePad.csproj" -c Release -o /app

FROM base AS publish
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "ScavengePad.dll"]