using System;
using System.Diagnostics;
using System.ComponentModel;
using Windows.ApplicationModel.Core;
using Urho;
//using Urho.Audio;
using Urho.Gui;
using Urho.SharpReality;
using Urho.Shapes;
using RabbitMQ.Client;
using System.Text;
using RabbitMQ.Client.Events;
using Urho.Resources;
using Windows.Foundation;

namespace Experiment1
{
    internal class Program
    {
        [MTAThread]
        static void Main() => CoreApplication.Run(
            new UrhoAppViewSource<Progam>(
                new ApplicationOptions("Data")));
    }

    public class Progam : StereoApplication
    {
        Node lampANode, textLampA, statusLampA;
        Node lampBNode, textLampB, statusLampB;
        Node acNode, textAc;
        //Material acMaterial;
        Text3D text3DA, status3DA;
        Text3D text3DB, status3DB;
        String perintah;
        ConnectionFactory factory;
        IConnection conn;
        bool toogles;
        bool lampAIsYellow, lampAIsGray, lampAIsOrange;
        bool lampBIsYellow, lampBIsGray, lampBIsOrange;
        private EventingBasicConsumer consumer;
        private IModel channel;

        public Progam(ApplicationOptions opts) : base(opts) { }

        protected override void Start()
        {

            // Create a basic scene, see StereoApplication
            base.Start();

            //activate RMQ receiver 
            //Rmqinit();

            // Allow tap gesture
            EnableGestureTapped = true;

            // Create Node for Lamp On
            lampANode = Scene.CreateChild("Lamp1");
            lampANode.Position = new Vector3(0.7f, 1, 4);
            lampANode.SetScale(0.2f); // 20cm

            // Create a static model component - Sphere:
            var lampOn = lampANode.CreateComponent<Sphere>();
            // Materials are usually more complicated than just textures, but for such
            // simple cases we can use quick FromImage method to create a material from an image.
            lampOn.SetMaterial(Material.FromColor(Color.Yellow));
            lampAIsYellow = true;
            lampAIsGray = false;
            lampAIsOrange = false;

            // Create Node for Lamp Off
            lampBNode = Scene.CreateChild("Lamp2");
            lampBNode.Position = new Vector3(0f, 1, 4);
            lampBNode.SetScale(0.2f);

            var lampOff = lampBNode.CreateComponent<Sphere>();
            lampOff.SetMaterial(Material.FromColor(Color.Gray));
            lampBIsYellow = false;
            lampBIsGray = true;
            lampBIsOrange = false;

            // Create Node for AC
            acNode = Scene.CreateChild("Aircon");
            acNode.Position = new Vector3(-1.5f, 1, 3f);
            acNode.Scale = new Vector3(0.2f, 0.2f, 0.5f); //x ke samping y ke atas z ke depan
            acNode.Rotation = new Quaternion(0, 0, 0); // rotate the object (x sumbu atas, y sumbu samping, z sumbu masuk)

            var acOn = acNode.CreateComponent<StaticModel>();
            acOn.Model = ResourceCache.GetModel("Models/ac.mdl");
            acOn.SetMaterial(Material.FromColor(Color.Blue));
            acOn.ViewMask = 0x80000000; //hide from raycasts


            textLampuSatu();
            statusLampuSatu();
            textLampuDua();
            statusLampuDua();

            /*
            // Get the message
            consumer.Received += (model, ea) =>
            {
                var body = ea.Body;
                var message = Encoding.UTF8.GetString(body);
                perintah = message;

                Debug.WriteLine(message);
                Debug.WriteLine(perintah);

                if (perintah == "sentence1: <s> BUKA BROWSER </s>\n")
                {
                    toogles = true; //Toogle for activate the command of on/off lamp
                    OnGestureTapped();
                    /*if (toogles == true)
                    {
                        OnGestureTapped();  //Call OnGestureTapped function
                    }
                }
                if (perintah == "sentence1: <s> MATIKAN LAMPU </s>\n")
                {
                    toogles = true; //Toogle for activate the command of on/off lamp
                    if (toogles == true)
                    {
                        OnGestureTapped();  //Call OnGestureTapped function
                    }
                }
                if (perintah == "sentence1: <s> REDUPKAN LAMPU </s>\n")
                {
                    toogles = true; //Toogle for activate the command of on/off lamp
                    if (toogles == true)
                    {
                        OnGestureTapped();  //Call OnGestureTapped function
                    }
                }
                if (perintah == "sentence1: <s> BUKA BROWSER </s>\n")
                {
                    toogles = true; //Toogle for activate the command of on/off lamp
                    if (toogles == true)
                    {
                        OnGestureTapped();  //Call OnGestureTapped function
                    }
                }
            };
            var queueName = "hello"; //channel.QueueDeclare().QueueName;
            channel.BasicConsume(queue: queueName,
                                 noAck: true,
                                 consumer: consumer);
                                 */
        }

        protected override void OnUpdate(float timeStep)
        {
            Ray cameraRay = RightCamera.GetScreenRay(0.5f, 0.5f);
            var result = Scene.GetComponent<Octree>().RaycastSingle(cameraRay, RayQueryLevel.Triangle, 100, DrawableFlags.Geometry, 0x70000000);
            //Debug.WriteLine("Result: " + result);
            if (result != null)
            {

            }
        }

        public override void OnGestureTapped()
        {
            Ray cameraRay = RightCamera.GetScreenRay(0.5f, 0.5f);
            var result = Scene.GetComponent<Octree>().RaycastSingle(cameraRay, RayQueryLevel.Triangle, 100, DrawableFlags.Geometry, 0x70000000);
            Debug.WriteLine("Result: " + result);
            if (result != null)
            {

                Debug.WriteLine(result.Value.Position.X);

                // Debug.WriteLine(result.Value.Position.Y);
                try
                {
                    if (result.Value.Position.X >= 0.5f)
                    {
                        //Debug.WriteLine(result.Value.Position.Z);
                        if (lampAIsYellow && (perintah == "sentence1: <s> REDUPKAN LAMPU </s>\n"))
                        {
                            lampANode.GetComponent<Sphere>().SetMaterial(Material.FromColor(Color.FromHex("FFA500")));
                            lampAIsYellow = false;
                            lampAIsGray = false;
                            lampAIsOrange = true;
                            //Debug.WriteLine(textLampOff.GetComponent.textLampOff);
                            text3DA.Text = "Lamp is On";
                            status3DA.Text = "Luminosity : Dimmed";
                        }
                        else
                        if (lampAIsOrange && (perintah == "sentence1: <s> TERANGKAN LAMPU </s>\n"))
                        {
                            lampANode.GetComponent<Sphere>().SetMaterial(Material.FromColor(Color.Yellow));
                            lampAIsYellow = true;
                            lampAIsGray = false;
                            lampAIsOrange = false;
                            text3DA.Text = "Lamp is On";
                            status3DA.Text = "Luminosity : Bright";
                        }

                        else
                        if ((lampAIsOrange || lampAIsYellow) && (perintah == "sentence1: <s> MATIKAN LAMPU </s>\n"))
                        {
                            lampANode.GetComponent<Sphere>().SetMaterial(Material.FromColor(Color.Gray));
                            lampAIsGray = true;
                            text3DA.Text = "Lamp is Off";
                            status3DA.Text = "Luminosity : Off";
                        }
                    }
                    if (result.Value.Position.X <= 0.1f)
                    {
                        // Debug.WriteLine(result.Value.Position.X);
                        if (lampBIsYellow)
                        {
                            lampBNode.GetComponent<Sphere>().SetMaterial(Material.FromColor(Color.Gray));
                            lampBIsYellow = false;
                            text3DB.Text = "Lamp is Off";
                            status3DB.Text = "Luminosity : Off";

                        }
                        else
                        {
                            lampBNode.GetComponent<Sphere>().SetMaterial(Material.FromColor(Color.Yellow));
                            lampBIsYellow = true;
                            text3DB.Text = "Lamp is On";
                            status3DB.Text = "Luminosity : Bright";

                        }
                    }
                }
                catch (NullReferenceException e)
                {
                    Debug.WriteLine("Error: " + e.Message.ToString());
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error: " + ex.Message.ToString());
                }

            }
            base.OnGestureTapped();
        }

        private async void launchURI_Click(object sender, Windows.UI.Xaml.RoutedEventArgs e)
        {
            // The URI to launch
            var uriBing = new Uri(@"http://www.google.com");

            // Launch the URI
            var success = await Windows.System.Launcher.LaunchUriAsync(uriBing);

            if (success)
            {
                // URI launched
            }
            else
            {
                // URI launch failed
            }
        }

         


        /*void Rmqinit()
        {
            //var factory = new ConnectionFactory() { HostName = "localhost"};
            //var server = "167.205.66.21"; // An install of RabbitMQ reachable from both clients
            //var password = "hololens";	
            //var username = "belva";
            //var factory = new ConnectionFactory { HostName = server, Password = password , Username = username};

            ConnectionFactory factory = new ConnectionFactory();
            factory.UserName = "raspi";
            factory.Password = "hololens";
            factory.VirtualHost = "/";
            factory.HostName = "172.20.10.11";

            conn = factory.CreateConnection();
            channel = conn.CreateModel();
            channel.ExchangeDeclare(exchange: "logs", type: "fanout");
            var queueName = "hello"; //channel.QueueDeclare().QueueName;
            channel.QueueBind(queue: queueName,
                              exchange: "logs",
                              routingKey: "");

            consumer = new EventingBasicConsumer(channel);
        }*/



        void textLampuSatu()
        {
            // Create text 
            textLampA = lampANode.CreateChild();
            text3DA = textLampA.CreateComponent<Text3D>();
            text3DA.HorizontalAlignment = HorizontalAlignment.Center;
            text3DA.VerticalAlignment = VerticalAlignment.Top;
            //text3D.ViewMask = 0x80000000; //hide from raycasts
            text3DA.Text = "Lamp is On";
            text3DA.SetFont(CoreAssets.Fonts.AnonymousPro, 26);
            text3DA.SetColor(Color.White);
            textLampA.Translate(new Vector3(0, -1f, -0.5f));
        }

        void statusLampuSatu()
        {
            //Create text Luminosity Status
            statusLampA = textLampA.CreateChild();
            status3DA = statusLampA.CreateComponent<Text3D>();
            status3DA.HorizontalAlignment = HorizontalAlignment.Center;
            status3DA.VerticalAlignment = VerticalAlignment.Top;
            //text3D.ViewMask = 0x80000000; //hide from raycasts
            status3DA.Text = "Luminosity : Bright";
            status3DA.SetFont(CoreAssets.Fonts.AnonymousPro, 26);
            status3DA.SetColor(Color.White);
            statusLampA.Translate(new Vector3(0, -0.5f, -0.5f));
        }


        void textLampuDua()
        {
            // Create text
            textLampB = lampBNode.CreateChild();
            text3DB = textLampB.CreateComponent<Text3D>();
            text3DB.HorizontalAlignment = HorizontalAlignment.Center;
            text3DB.VerticalAlignment = VerticalAlignment.Top;
            //text3D.ViewMask = 0x80000000; //hide from raycasts
            text3DB.Text = "Lamp is Off";
            text3DB.SetFont(CoreAssets.Fonts.AnonymousPro, 26);
            text3DB.SetColor(Color.White);
            textLampB.Translate(new Vector3(0, -1f, -0.5f));
        }

        void statusLampuDua()
        {
            //Create text Luminosity Status
            statusLampB = textLampB.CreateChild();
            status3DB = statusLampB.CreateComponent<Text3D>();
            status3DB.HorizontalAlignment = HorizontalAlignment.Center;
            status3DB.VerticalAlignment = VerticalAlignment.Top;
            //text3D.ViewMask = 0x80000000; //hide from raycasts
            status3DB.Text = "Luminosity : Off";
            status3DB.SetFont(CoreAssets.Fonts.AnonymousPro, 26);
            status3DB.SetColor(Color.White);
            statusLampB.Translate(new Vector3(0, -0.5f, -0.5f));
        }

    }
}